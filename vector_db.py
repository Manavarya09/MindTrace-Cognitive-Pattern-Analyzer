"""
Vector Database Integration for MindTrace
Pinecone & Weaviate for semantic search and embeddings
"""
from pinecone import Pinecone, ServerlessSpec
from weaviate import Client
from typing import List, Dict, Optional, Any
import numpy as np
import os


class VectorDBManager:
    def __init__(self, provider: str = "pinecone"):
        self.provider = provider
        self._setup_client()
    
    def _setup_client(self):
        if self.provider == "pinecone":
            api_key = os.getenv("PINECONE_API_KEY")
            environment = os.getenv("PINECONE_ENVIRONMENT", "us-west1-gcp")
            
            self.client = Pinecone(api_key=api_key)
            
            if "mindtrace" not in self.client.list_indexes().names():
                self.client.create_index(
                    name="mindtrace",
                    dimension=1536,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region=environment
                    )
                )
            
            self.index = self.client.Index("mindtrace")
        
        elif self.provider == "weaviate":
            self.client = Client(
                url=os.getenv("WEAVIATE_URL", "http://localhost:8080"),
                auth_client_secret=os.getenv("WEAVIATE_API_KEY")
            )
            
            schema = {
                "class": "CognitivePattern",
                "description": "Cognitive analysis patterns",
                "vectorizer": "text2vec-transformers",
                "moduleConfig": {
                    "text2vec-transformers": {
                        "vectorizeClassName": False
                    }
                },
                "properties": [
                    {"name": "text", "dataType": ["text"]},
                    {"name": "user_id", "dataType": ["text"]},
                    {"name": "pattern_type", "dataType": ["text"]},
                    {"name": "timestamp", "dataType": ["date"]},
                    {"name": "metadata", "dataType": ["object"]}
                ]
            }
            
            if not self.client.schema.exists("CognitivePattern"):
                self.client.schema.create_class(schema)
    
    def add_vectors(
        self,
        vectors: List[np.ndarray],
        metadata: List[Dict],
        ids: Optional[List[str]] = None
    ):
        if self.provider == "pinecone":
            if ids is None:
                ids = [f"vec_{i}" for i in range(len(vectors))]
            
            vectors_list = [v.tolist() if isinstance(v, np.ndarray) else v for v in vectors]
            
            self.index.upsert(
                vectors=zip(ids, vectors_list, metadata)
            )
        
        elif self.provider == "weaviate":
            with self.client.batch as batch:
                for i, (vector, meta) in enumerate(zip(vectors, metadata)):
                    self.client.data_object.create(
                        class_name="CognitivePattern",
                        data_object=meta,
                        vector=vector.tolist() if isinstance(vector, np.ndarray) else vector
                    )
    
    def search(
        self,
        query_vector: np.ndarray,
        top_k: int = 10,
        filter_criteria: Optional[Dict] = None
    ) -> List[Dict]:
        if self.provider == "pinecone":
            query_vector = query_vector.tolist() if isinstance(query_vector, np.ndarray) else query_vector
            
            results = self.index.query(
                vector=query_vector,
                top_k=top_k,
                filter=filter_criteria,
                include_metadata=True
            )
            
            return [
                {
                    "id": match.id,
                    "score": match.score,
                    "metadata": match.metadata
                }
                for match in results.matches
            ]
        
        elif self.provider == "weaviate":
            results = self.client.query.get(
                "CognitivePattern",
                ["text", "user_id", "pattern_type", "timestamp", "metadata"]
            ).with_near_vector(
                {"vector": query_vector.tolist() if isinstance(query_vector, np.ndarray) else query_vector}
            ).with_limit(top_k).do()
            
            return results.get("data", {}).get("Get", {}).get("CognitivePattern", [])
    
    def delete_vectors(self, ids: List[str]):
        if self.provider == "pinecone":
            self.index.delete(ids=ids)
        elif self.provider == "weaviate":
            for id in ids:
                self.client.data_object.delete(id)
    
    def get_index_stats(self) -> Dict:
        if self.provider == "pinecone":
            return self.index.describe_index_stats()
        return {}


class SemanticSearchEngine:
    def __init__(self, vector_db: VectorDBManager):
        self.vector_db = vector_db
    
    def find_similar_patterns(
        self,
        text: str,
        embedding: np.ndarray,
        user_id: Optional[str] = None,
        top_k: int = 5
    ) -> List[Dict]:
        filters = {}
        if user_id:
            filters["user_id"] = {"$eq": user_id}
        
        results = self.vector_db.search(
            query_vector=embedding,
            top_k=top_k,
            filter_criteria=filters if filters else None
        )
        
        return results
    
    def find_contradictions(
        self,
        text: str,
        embedding: np.ndarray,
        threshold: float = 0.3
    ) -> List[Dict]:
        results = self.vector_db.search(
            query_vector=embedding,
            top_k=20
        )
        
        contradictions = []
        for result in results:
            if result.get("score", 0) < threshold:
                contradictions.append(result)
        
        return contradictions
    
    def cluster_similar_thoughts(
        self,
        embeddings: List[np.ndarray],
        metadata: List[Dict],
        min_cluster_size: int = 3
    ):
        from sklearn.cluster import DBSCAN
        
        clustering = DBSCAN(eps=0.3, min_samples=min_cluster_size).fit(embeddings)
        
        clusters = {}
        for i, label in enumerate(clustering.labels_):
            if label == -1:
                continue
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(metadata[i])
        
        return clusters


class EmbeddingCache:
    def __init__(self, vector_db: VectorDBManager):
        self.vector_db = vector_db
        self.local_cache = {}
    
    def get_or_create(
        self,
        text: str,
        embedding: np.ndarray,
        user_id: str,
        metadata: Dict
    ) -> str:
        text_hash = str(hash(text))
        
        if text_hash in self.local_cache:
            return self.local_cache[text_hash]
        
        vector_id = f"{user_id}_{text_hash}"
        
        self.vector_db.add_vectors(
            vectors=[embedding],
            metadata=[{**metadata, "text": text}],
            ids=[vector_id]
        )
        
        self.local_cache[text_hash] = vector_id
        return vector_id


if __name__ == "__main__":
    vdb = VectorDBManager(provider="pinecone")
    search = SemanticSearchEngine(vdb)
    print("Vector database initialized")
