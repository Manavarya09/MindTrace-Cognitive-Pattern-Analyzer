"""
Redis Caching Layer for MindTrace
High-performance distributed caching with Redis
"""
import redis
import json
import hashlib
from typing import Any, Optional, Callable
from functools import wraps
from datetime import timedelta
import pickle
import numpy as np


class RedisCache:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5
        )
        self.default_ttl = 3600
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        key_data = f"{prefix}:{args}:{sorted(kwargs.items())}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        try:
            data = self.client.get(key)
            if data:
                return pickle.loads(data.encode('latin1'))
        except Exception as e:
            print(f"Cache get error: {e}")
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        try:
            ttl = ttl or self.default_ttl
            serialized = pickle.dumps(value)
            self.client.setex(key, ttl, serialized)
            return True
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        try:
            self.client.delete(key)
            return True
        except:
            return False
    
    def clear_pattern(self, pattern: str) -> int:
        try:
            keys = self.client.keys(pattern)
            if keys:
                return self.client.delete(*keys)
        except:
            pass
        return 0
    
    def get_stats(self) -> dict:
        try:
            info = self.client.info()
            return {
                "connected": True,
                "keys": self.client.dbsize(),
                "memory_used": info.get("used_memory_human"),
                "hits": info.get("keyspace_hits", 0),
                "misses": info.get("keyspace_misses", 0),
                "hit_rate": info.get("keyspace_hits", 1) / max(info.get("keyspace_hits", 1) + info.get("keyspace_misses", 1), 1)
            }
        except:
            return {"connected": False}


def cached(ttl: int = 3600, prefix: str = "mindtrace"):
    def decorator(func: Callable) -> Callable:
        cache = RedisCache()
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = cache._generate_key(prefix, *args, **kwargs)
            result = cache.get(key)
            
            if result is not None:
                return result
            
            result = func(*args, **kwargs)
            cache.set(key, result, ttl)
            return result
        
        wrapper.cache = cache
        wrapper.clear_cache = lambda: cache.clear_pattern(f"{prefix}:*")
        return wrapper
    return decorator


class CacheManager:
    def __init__(self):
        self.cache = RedisCache()
        self.patterns = {
            "analysis": "analysis:*",
            "sentiment": "sentiment:*",
            "topics": "topics:*",
            "embeddings": "embeddings:*",
            "user": "user:*"
        }
    
    def cache_analysis(self, text_hash: str, result: dict, ttl: int = 1800):
        key = f"analysis:{text_hash}"
        self.cache.set(key, result, ttl)
    
    def get_cached_analysis(self, text_hash: str) -> Optional[dict]:
        return self.cache.get(f"analysis:{text_hash}")
    
    def cache_embeddings(self, text: str, embeddings: np.ndarray, ttl: int = 86400):
        key = f"embeddings:{hashlib.md5(text.encode()).hexdigest()}"
        self.cache.set(key, embeddings, ttl)
    
    def get_cached_embeddings(self, text: str) -> Optional[np.ndarray]:
        return self.cache.get(f"embeddings:{hashlib.md5(text.encode()).hexdigest()}")
    
    def invalidate_user_cache(self, user_id: int):
        for pattern in self.patterns.values():
            self.cache.clear_pattern(f"{pattern.replace('*', str(user_id))}*")
    
    def get_cache_stats(self) -> dict:
        return self.cache.get_stats()


cache_manager = CacheManager()
