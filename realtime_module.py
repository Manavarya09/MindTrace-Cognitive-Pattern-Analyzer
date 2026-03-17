# MindTrace - Real-time Analysis Module

import time
from datetime import datetime

class RealTimeAnalyzer:
    def __init__(self):
        self.history = []
    
    def analyze_stream(self, text, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now()
        
        # Quick sentiment
        scores = sia.polarity_scores(text)
        
        result = {
            "timestamp": timestamp,
            "text": text,
            "polarity": scores["compound"],
            "sentiment": "positive" if scores["compound"] > 0.05 else "negative" if scores["compound"] < -0.05 else "neutral"
        }
        
        self.history.append(result)
        
        return result
    
    def get_moving_average(self, window=10):
        if len(self.history) < window:
            return None
        
        recent = self.history[-window:]
        return sum(r["polarity"] for r in recent) / window
    
    def detect_shift(self, threshold=0.2):
        if len(self.history) < 20:
            return None
        
        first_half = sum(r["polarity"] for r in self.history[:10]) / 10
        second_half = sum(r["polarity"] for r in self.history[10:20]) / 10
        
        shift = second_half - first_half
        
        if abs(shift) > threshold:
            return {"detected": True, "shift": shift, "direction": "positive" if shift > 0 else "negative"}
        
        return {"detected": False}

# Real-time dashboard widget
class LiveDashboard:
    def __init__(self):
        self.analyzer = RealTimeAnalyzer()
    
    def add_entry(self, text):
        return self.analyzer.analyze_stream(text)
    
    def get_stats(self):
        return {
            "total_entries": len(self.analyzer.history),
            "moving_avg": self.analyzer.get_moving_average(),
            "recent_shift": self.analyzer.detect_shift()
        }

live_dashboard = LiveDashboard()
print("LiveDashboard ready!")
