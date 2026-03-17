# MindTrace - Cache and Optimization Module

from functools import lru_cache
import hashlib

class AnalysisCache:
    def __init__(self):
        self.cache = {}
        self.hits = 0
        self.misses = 0
    
    def get_key(self, text):
        return hashlib.md5(text.encode()).hexdigest()
    
    def get(self, text):
        key = self.get_key(text)
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None
    
    def set(self, text, result):
        key = self.get_key(text)
        self.cache[key] = result
    
    def get_stats(self):
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {"hits": self.hits, "misses": self.misses, "hit_rate": f"{hit_rate:.1f}%", "cache_size": len(self.cache)}
    
    def clear(self):
        self.cache = {}
        self.hits = 0
        self.misses = 0

cache = AnalysisCache()
print("AnalysisCache ready!")
