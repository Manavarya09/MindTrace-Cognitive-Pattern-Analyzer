# MindTrace - ML Pipeline Module

"""
Complete ML pipeline with model training and deployment
"""

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.metrics import classification_report, mean_squared_error, r2_score

class MLPipeline:
    """End-to-end ML pipeline"""
    
    def __init__(self):
        self.models = {}
        self.feature_extractor = TfidfVectorizer(max_features=500)
    
    def prepare_features(self, texts):
        return self.feature_extractor.fit_transform(texts)
    
    def train_sentiment_model(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        
        self.models['sentiment'] = {
            'model': model,
            'report': classification_report(y_test, y_pred),
            'accuracy': model.score(X_test, y_test)
        }
        
        return self.models['sentiment']
    
    def train_regressor(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        
        self.models['regressor'] = {
            'model': model,
            'mse': mean_squared_error(y_test, y_pred),
            'r2': r2_score(y_test, y_pred)
        }
        
        return self.models['regressor']
    
    def predict(self, text, model_type='sentiment'):
        if model_type not in self.models:
            return None
        
        X = self.feature_extractor.transform([text])
        return self.models[model_type]['model'].predict(X)
    
    def cross_validate(self, X, y, cv=5):
        model = RandomForestClassifier(n_estimators=50, random_state=42)
        scores = cross_val_score(model, X, y, cv=cv)
        return {"scores": scores, "mean": scores.mean(), "std": scores.std()}

pipeline = MLPipeline()
print("ML Pipeline ready!")
