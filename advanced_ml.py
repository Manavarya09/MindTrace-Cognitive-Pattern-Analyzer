# MindTrace - Advanced ML Models

"""
Transformer-based sentiment analysis and advanced NLP
"""

# Try to import transformers
try:
    from transformers import pipeline, AutoTokenizer, AutoModel
    TRANSFORMERS_AVAILABLE = True
except:
    TRANSFORMERS_AVAILABLE = False

class TransformerSentiment:
    """BERT-based sentiment analysis"""
    
    def __init__(self):
        if TRANSFORMERS_AVAILABLE:
            self.analyzer = pipeline("sentiment-analysis", 
                                  model="distilbert-base-uncased-finetuned-sst-2-english")
        else:
            self.analyzer = None
    
    def analyze(self, text):
        if not self.analyzer:
            return {"error": "Transformers not available"}
        
        result = self.analyzer(text)[0]
        return {
            "label": result["label"].lower(),
            "score": result["score"]
        }
    
    def batch_analyze(self, texts, batch_size=32):
        if not self.analyzer:
            return [{"error": "Transformers not available"}] * len(texts)
        
        results = self.analyzer(texts, batch_size=batch_size)
        return [{"label": r["label"].lower(), "score": r["score"]} for r in results]

class EmotionClassifier:
    """Multi-label emotion classification"""
    
    def __init__(self):
        if TRANSFORMERS_AVAILABLE:
            self.classifier = pipeline("text-classification", 
                                     model="j-hartmann/emotion-english-distilroberta-base",
                                     top_k=None)
        else:
            self.classifier = None
    
    def classify(self, text):
        if not self.classifier:
            return {"error": "Transformers not available"}
        
        result = self.classifier(text)[0]
        emotions = {r["label"]: r["score"] for r in result}
        return emotions
    
    def get_dominant(self, text):
        emotions = self.classify(text)
        if "error" in emotions:
            return None
        
        return max(emotions, key=emotions.get)

class ZeroShotClassifier:
    """Zero-shot classification for custom categories"""
    
    def __init__(self):
        if TRANSFORMERS_AVAILABLE:
            self.classifier = pipeline("zero-shot-classification")
        else:
            self.classifier = None
    
    def classify(self, text, labels):
        if not self.classifier:
            return {"error": "Transformers not available"}
        
        result = self.classifier(text, labels)
        return {
            "labels": result["labels"],
            "scores": result["scores"]
        }

# Initialize if available
bert_sentiment = TransformerSentiment() if TRANSFORMERS_AVAILABLE else None
emotion_classifier = EmotionClassifier() if TRANSFORMERS_AVAILABLE else None
zero_shot = ZeroShotClassifier() if TRANSFORMERS_AVAILABLE else None

print(f"Advanced ML models loaded: {TRANSFORMERS_AVAILABLE}")
