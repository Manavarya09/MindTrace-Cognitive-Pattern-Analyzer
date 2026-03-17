"""
LangChain Integration with LLM Models
Advanced AI-powered cognitive analysis using GPT and Claude
"""
from langchain.chains import LLMChain, ConversationalRetrievalChain
from langchain.llms import OpenAI, Anthropic
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.agents import AgentExecutor, Tool
from langchain.memory import ConversationBufferMemory, VectorStoreRetrieverMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone, Chroma, FAISS
from typing import List, Dict, Optional, Any
import os


class LangChainAnalyzer:
    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-4",
        temperature: float = 0.7
    ):
        self.provider = provider
        self.model = model
        
        if provider == "openai":
            self.llm = OpenAI(
                model=model,
                temperature=temperature,
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
        elif provider == "anthropic":
            self.llm = Anthropic(
                model=model,
                temperature=temperature,
                anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    def create_prompt_template(self, template: str) -> PromptTemplate:
        return PromptTemplate(
            template=template,
            input_variables=["text", "context"]
        )
    
    def analyze_with_llm(
        self,
        text: str,
        analysis_type: str = "cognitive"
    ) -> Dict[str, Any]:
        prompts = {
            "cognitive": """Analyze the following text for cognitive patterns:
            {text}
            
            Identify:
            1. Thinking style (analytical, creative, practical, etc.)
            2. Emotional undertones
            3. Key themes and concepts
            4. Potential biases
            5. Cognitive strengths and weaknesses""",
            
            "emotional": """Perform deep emotional analysis on:
            {text}
            
            Provide:
            1. Primary emotions detected
            2. Emotional intensity (1-10)
            3. Emotional triggers
            4. Mood patterns
            5. Sentiment summary""",
            
            "productivity": """Analyze productivity insights from:
            {text}
            
            Identify:
            1. Task completion indicators
            2. Time management patterns
            3. Focus areas
            4. Potential bottlenecks
            5. Recommendations""",
            
            "behavioral": """Analyze behavioral patterns in:
            {text}
            
            Find:
            1. Recurring behaviors
            2. Habit formation indicators
            3. Behavioral triggers
            4. Consistency patterns
            5. Change indicators"""
        }
        
        prompt = prompts.get(analysis_type, prompts["cognitive"])
        chain = LLMChain(llm=self.llm, prompt=self.create_prompt_template(prompt))
        
        result = chain.run(text=text)
        
        return {
            "analysis_type": analysis_type,
            "result": result,
            "model": f"{self.provider}/{self.model}"
        }
    
    def create_rag_system(
        self,
        documents: List[str],
        vector_store_type: str = "chroma"
    ) -> ConversationalRetrievalChain:
        docs = [
            Document(page_content=doc)
            for doc in documents
        ]
        
        chunks = self.text_splitter.split_documents(docs)
        
        if vector_store_type == "chroma":
            vectorstore = Chroma.from_documents(chunks, self.embeddings)
        elif vector_store_type == "faiss":
            vectorstore = FAISS.from_documents(chunks, self.embeddings)
        elif vector_store_type == "pinecone":
            vectorstore = Pinecone.from_documents(
                chunks,
                self.embeddings,
                index_name="mindtrace"
            )
        
        retriever = vectorstore.as_retriever()
        
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a cognitive analysis expert. Use the provided context to answer questions about the user's thinking patterns, emotional trends, and behavioral insights."),
            ("human", "{question}")
        ])
        
        chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": qa_prompt}
        )
        
        return chain
    
    def ask_cognitive_question(
        self,
        question: str,
        context: Optional[List[str]] = None
    ) -> str:
        if context:
            chain = self.create_rag_system(context)
            return chain.run(question)
        
        qa_prompt = f"""Based on the cognitive analysis data, answer:
        {question}
        
        Provide specific, actionable insights."""
        
        return self.llm(qa_prompt)
    
    def generate_insights_summary(
        self,
        analysis_results: List[Dict]
    ) -> str:
        summary_prompt = """Synthesize the following cognitive analysis results into a comprehensive summary:
        
        {results}
        
        Include:
        1. Key findings
        2. Actionable recommendations
        3. Potential areas for improvement
        4. Overall cognitive profile"""
        
        results_text = "\n".join([str(r) for r in analysis_results])
        prompt = summary_prompt.format(results=results_text)
        
        return self.llm(prompt)
    
    def detect_anomalies_with_llm(
        self,
        text: str,
        baseline_patterns: List[str]
    ) -> Dict[str, Any]:
        anomaly_prompt = f"""Compare the following text against these baseline patterns:
        
        Text: {text}
        
        Baseline patterns:
        {chr(10).join(baseline_patterns)}
        
        Identify any anomalies, unusual patterns, or significant deviations.
        Rate the anomaly severity from 0-10."""
        
        result = self.llm(anomaly_prompt)
        
        return {
            "text": text,
            "anomaly_analysis": result,
            "baseline_count": len(baseline_patterns)
        }


class CognitiveAgent:
    def __init__(self):
        self.analyzer = LangChainAnalyzer()
        self.tools = []
        self._setup_tools()
    
    def _setup_tools(self):
        self.tools = [
            Tool(
                name="Analyze Thinking Patterns",
                func=lambda x: self.analyzer.analyze_with_llm(x, "cognitive"),
                description="Analyze cognitive thinking patterns in text"
            ),
            Tool(
                name="Detect Emotions",
                func=lambda x: self.analyzer.analyze_with_llm(x, "emotional"),
                description="Detect emotional patterns and sentiment"
            ),
            Tool(
                name="Productivity Analysis",
                func=lambda x: self.analyzer.analyze_with_llm(x, "productivity"),
                description="Analyze productivity and task completion patterns"
            ),
            Tool(
                name="Behavioral Analysis",
                func=lambda x: self.analyzer.analyze_with_llm(x, "behavioral"),
                description="Analyze behavioral patterns and habits"
            )
        ]
    
    def run_analysis(self, text: str) -> Dict[str, Any]:
        results = {}
        for tool in self.tools:
            results[tool.name] = tool.func(text)
        return results


if __name__ == "__main__":
    agent = CognitiveAgent()
    sample_text = "Today I completed the machine learning model and felt really accomplished. However, I'm worried about the data quality issues we discovered."
    results = agent.run_analysis(sample_text)
    print(results)
