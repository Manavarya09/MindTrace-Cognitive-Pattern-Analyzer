"""
WebSocket API for Real-time MindTrace
FastAPI WebSocket for live cognitive analysis streaming
"""
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Set
import json
from datetime import datetime
import uuid

from mindtrace import CognitiveAnalyzer
from mindtrace.advanced_nlp import AdvancedNLPProcessor


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_sessions: Dict[str, str] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
    
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
    
    async def send_personal_message(self, message: dict, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(message)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_json(message)
    
    def get_active_count(self) -> int:
        return len(self.active_connections)


manager = ConnectionManager()
analyzer = CognitiveAnalyzer()
nlp = AdvancedNLPProcessor()

app = FastAPI(title="MindTrace WebSocket API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "service": "MindTrace WebSocket API",
        "version": "2.0.0",
        "active_connections": manager.get_active_count()
    }


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    
    try:
        await websocket.send_json({
            "type": "connected",
            "client_id": client_id,
            "timestamp": datetime.now().isoformat()
        })
        
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            await process_message(client_id, message)
            
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast({
            "type": "disconnect",
            "client_id": client_id,
            "timestamp": datetime.now().isoformat()
        })


async def process_message(client_id: str, message: dict):
    msg_type = message.get("type")
    
    if msg_type == "analyze":
        text = message.get("text", "")
        
        await manager.send_personal_message({
            "type": "analysis_start",
            "text": text[:50] + "...",
            "timestamp": datetime.now().isoformat()
        }, client_id)
        
        sentiment = analyzer.analyze_sentiment(text)
        emotions = analyzer.detect_emotions(text)
        topics = nlp.extract_topics([text])
        
        await manager.send_personal_message({
            "type": "analysis_complete",
            "result": {
                "sentiment": sentiment,
                "emotions": emotions,
                "topics": topics
            },
            "timestamp": datetime.now().isoformat()
        }, client_id)
    
    elif msg_type == "bulk_analyze":
        texts = message.get("texts", [])
        
        for i, text in enumerate(texts):
            result = analyzer.analyze(text)
            
            await manager.send_personal_message({
                "type": "batch_progress",
                "current": i + 1,
                "total": len(texts),
                "result": result,
                "timestamp": datetime.now().isoformat()
            }, client_id)
        
        await manager.send_personal_message({
            "type": "batch_complete",
            "total_processed": len(texts),
            "timestamp": datetime.now().isoformat()
        }, client_id)
    
    elif msg_type == "stream_text":
        text = message.get("text", "")
        
        for i in range(0, len(text), 50):
            chunk = text[i:i+50]
            
            await manager.send_personal_message({
                "type": "stream_chunk",
                "chunk": chunk,
                "position": i,
                "timestamp": datetime.now().isoformat()
            }, client_id)
            
            await asyncio.sleep(0.1)
        
        await manager.send_personal_message({
            "type": "stream_complete",
            "timestamp": datetime.now().isoformat()
        }, client_id)
    
    elif msg_type == "subscribe":
        pattern_type = message.get("pattern_type")
        
        await manager.send_personal_message({
            "type": "subscribed",
            "pattern_type": pattern_type,
            "timestamp": datetime.now().isoformat()
        }, client_id)
    
    elif msg_type == "ping":
        await manager.send_personal_message({
            "type": "pong",
            "timestamp": datetime.now().isoformat()
        }, client_id)


@app.get("/stats")
async def get_stats():
    return {
        "active_connections": manager.get_active_count(),
        "server_time": datetime.now().isoformat()
    }


@app.post("/broadcast")
async def broadcast_message(message: dict):
    await manager.broadcast(message)
    return {"status": "broadcasted"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
