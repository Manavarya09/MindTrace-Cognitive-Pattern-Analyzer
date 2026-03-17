"""
Knowledge Graph Module for MindTrace
Graph-based cognitive pattern analysis using NetworkX and RDF
"""
import networkx as nx
from collections import defaultdict
from typing import List, Dict, Set, Optional, Tuple
import pandas as pd
from datetime import datetime
import json


class CognitiveKnowledgeGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.entity_types = [
            "person", "concept", "emotion", "behavior",
            "topic", "pattern", "memory", "relationship"
        ]
        
        self.relation_types = [
            "feels", "thinks", "does", "relates_to",
            "causes", "implies", "contradicts", "similar_to"
        ]
    
    def add_entity(
        self,
        entity_id: str,
        entity_type: str,
        properties: Optional[Dict] = None
    ):
        properties = properties or {}
        self.graph.add_node(
            entity_id,
            type=entity_type,
            properties=properties,
            created_at=datetime.now().isoformat()
        )
    
    def add_relation(
        self,
        source_id: str,
        target_id: str,
        relation_type: str,
        weight: float = 1.0,
        properties: Optional[Dict] = None
    ):
        if not self.graph.has_node(source_id):
            self.add_entity(source_id, "unknown")
        if not self.graph.has_node(target_id):
            self.add_entity(target_id, "unknown")
        
        self.graph.add_edge(
            source_id,
            target_id,
            relation=relation_type,
            weight=weight,
            properties=properties or {},
            created_at=datetime.now().isoformat()
        )
    
    def extract_from_text(
        self,
        text: str,
        entities: List[Dict],
        relations: List[Dict]
    ):
        for entity in entities:
            self.add_entity(
                entity["id"],
                entity.get("type", "concept"),
                entity.get("properties", {})
            )
        
        for relation in relations:
            self.add_relation(
                relation["source"],
                relation["target"],
                relation.get("type", "relates_to"),
                relation.get("weight", 1.0),
                relation.get("properties", {})
            )
    
    def find_paths(
        self,
        source_id: str,
        target_id: str,
        max_length: int = 3
    ) -> List[List[str]]:
        try:
            paths = list(nx.all_simple_paths(
                self.graph,
                source_id,
                target_id,
                cutoff=max_length
            ))
            return paths
        except nx.NetworkXNoPath:
            return []
    
    def find_central_entities(
        self,
        entity_type: Optional[str] = None,
        top_n: int = 10
    ) -> List[Tuple[str, float]]:
        if entity_type:
            nodes = [
                n for n, d in self.graph.nodes(data=True)
                if d.get("type") == entity_type
            ]
            subgraph = self.graph.subgraph(nodes)
        else:
            subgraph = self.graph
        
        centrality = nx.degree_centrality(subgraph)
        
        sorted_entities = sorted(
            centrality.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]
        
        return sorted_entities
    
    def find_communities(self) -> List[Set[str]]:
        if self.graph.number_of_nodes() < 2:
            return []
        
        undirected = self.graph.to_undirected()
        
        try:
            communities = list(nx.community.louvain_communities(undirected))
            return communities
        except:
            return []
    
    def detect_cycles(self) -> List[List[str]]:
        try:
            cycles = list(nx.simple_cycles(self.graph))
            return cycles
        except:
            return []
    
    def get_entity_neighbors(
        self,
        entity_id: str,
        relation_type: Optional[str] = None,
        max_depth: int = 1
    ) -> Dict:
        neighbors = defaultdict(list)
        
        for depth in range(1, max_depth + 1):
            if depth == 1:
                current = [entity_id]
            else:
                current = list(neighbors[depth - 1])
            
            for node in current:
                if self.graph.has_node(node):
                    for neighbor in self.graph.neighbors(node):
                        edge_data = self.graph.get_edge_data(node, neighbor)
                        rel_type = edge_data.get("relation", "unknown")
                        
                        if relation_type is None or rel_type == relation_type:
                            neighbors[depth].append({
                                "entity": neighbor,
                                "relation": rel_type,
                                "weight": edge_data.get("weight", 1.0)
                            })
        
        return dict(neighbors)
    
    def analyze_temporal_patterns(
        self,
        entity_id: str
    ) -> Dict:
        if not self.graph.has_node(entity_id):
            return {}
        
        edges_from = list(self.graph.predecessors(entity_id))
        edges_to = list(self.graph.successors(entity_id))
        
        timestamps = []
        for edge in edges_from + edges_to:
            edge_data = self.graph.get_edge_data(edge, entity_id) or \
                        self.graph.get_edge_data(entity_id, edge)
            if edge_data and "created_at" in edge_data:
                timestamps.append(edge_data["created_at"])
        
        return {
            "entity_id": entity_id,
            "connections_in": len(edges_from),
            "connections_out": len(edges_to),
            "total_connections": len(edges_from) + len(edges_to),
            "first_seen": min(timestamps) if timestamps else None,
            "last_seen": max(timestamps) if timestamps else None
        }
    
    def export_to_json(self, path: str):
        data = nx.node_link_data(self.graph)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    
    def import_from_json(self, path: str):
        with open(path, "r") as f:
            data = json.load(f)
        self.graph = nx.node_link_graph(data)
    
    def get_subgraph(
        self,
        entity_ids: List[str]
    ) -> nx.DiGraph:
        return self.graph.subgraph(entity_ids)
    
    def visualize_as_cytoscape(self) -> Dict:
        nodes = [
            {
                "data": {
                    "id": node,
                    "label": node,
                    "type": self.graph.nodes[node].get("type", "unknown")
                }
            }
            for node in self.graph.nodes()
        ]
        
        edges = [
            {
                "data": {
                    "source": source,
                    "target": target,
                    "relation": data.get("relation", "unknown"),
                    "weight": data.get("weight", 1.0)
                }
            }
            for source, target, data in self.graph.edges(data=True)
        ]
        
        return {"nodes": nodes, "edges": edges}


class GraphPatternDetector:
    def __init__(self, graph: CognitiveKnowledgeGraph):
        self.graph = graph
    
    def find_emotion_concept_links(self) -> List[Dict]:
        emotion_nodes = [
            n for n, d in self.graph.graph.nodes(data=True)
            if d.get("type") == "emotion"
        ]
        
        links = []
        for emotion in emotion_nodes:
            neighbors = self.graph.graph.neighbors(emotion)
            for neighbor in neighbors:
                neighbor_type = self.graph.graph.nodes[neighbor].get("type")
                links.append({
                    "emotion": emotion,
                    "concept": neighbor,
                    "type": neighbor_type
                })
        
        return links
    
    def find_thought_clusters(self, min_size: int = 3) -> List[List[str]]:
        communities = self.graph.find_communities()
        return [list(c) for c in communities if len(c) >= min_size]
    
    def find_causal_chains(self) -> List[List[str]]:
        chains = []
        
        for node in self.graph.graph.nodes():
            paths = self.graph.find_paths(node, node, max_length=4)
            for path in paths:
                if len(path) > 2:
                    chains.append(path)
        
        return chains
    
    def compute_graph_metrics(self) -> Dict:
        g = self.graph.graph
        
        if g.number_of_nodes() == 0:
            return {}
        
        return {
            "total_nodes": g.number_of_nodes(),
            "total_edges": g.number_of_edges(),
            "density": nx.density(g),
            "avg_clustering": nx.average_clustering(g.to_undirected()),
            "is_directed": g.is_directed(),
            "is_connected": nx.is_weakly_connected(g)
        }


if __name__ == "__main__":
    kg = CognitiveKnowledgeGraph()
    
    kg.add_entity("user_1", "person", {"name": "John"})
    kg.add_entity("anxiety", "emotion", {"intensity": "high"})
    kg.add_entity("work", "topic", {"category": "professional"})
    
    kg.add_relation("user_1", "anxiety", "feels", weight=0.8)
    kg.add_relation("anxiety", "work", "causes", weight=0.6)
    
    print(f"Central entities: {kg.find_central_entities()}")
    print(f"Graph metrics: {GraphPatternDetector(kg).compute_graph_metrics()}")
