# MindTrace - Advanced NLP Analysis Module
# Topic Modeling, NER, Word Embeddings, Forecasting

import nbformat
from nbformat import v4

nb = v4.new_notebook()

# Title
nb.cells.append(v4.new_markdown_cell('# MindTrace - Advanced NLP Extensions'))
nb.cells.append(v4.new_markdown_cell('## Advanced Analysis Module'))

# Topic Modeling
nb.cells.append(v4.new_markdown_cell('### 1. Topic Modeling with LDA'))
code = '''class TopicModeler:
    def __init__(self):
        pass
    
    def create_topics(self, texts, n_topics=5):
        vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=500)
        doc_term = vectorizer.fit_transform(texts)
        
        lda = LatentDirichletAllocation(n_components=n_topics, random_state=42, max_iter=20)
        lda.fit(doc_term)
        
        feature_names = vectorizer.get_feature_names_out()
        topics = {}
        for idx, topic in enumerate(lda.components_):
            top_words = [feature_names[i] for i in topic.argsort()[:-11:-1]]
            topics[f"Topic {idx+1}"] = top_words
        
        doc_topics = lda.transform(doc_term)
        
        return {"topics": topics, "doc_topics": doc_topics, "model": lda, "vectorizer": vectorizer}
    
    def get_document_topics(self, doc_topics):
        return [f"Topic {idx+1}" for idx in doc_topics.argmax(axis=1)]

topic_modeler = TopicModeler()
print("TopicModeler ready!")'''
nb.cells.append(v4.new_code_cell(code))

# Advanced NER
nb.cells.append(v4.new_markdown_cell('### 2. Named Entity Recognition'))
code = '''class AdvancedNER:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def extract_entities(self, text):
        doc = self.nlp(text)
        entities = {"PERSON": [], "ORG": [], "GPE": [], "DATE": [], "TIME": [], 
                   "MONEY": [], "PERCENT": [], "EVENT": [], "WORK_OF_ART": []}
        
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)
        
        return entities
    
    def extract_all(self, df):
        results = df["text"].apply(self.extract_entities)
        return results

advanced_ner = AdvancedNER()
print("AdvancedNER ready!")'''
nb.cells.append(v4.new_code_cell(code))

# Word Embeddings
nb.cells.append(v4.new_markdown_cell('### 3. Word Embeddings and Similarity'))
code = '''class WordEmbeddings:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def get_vector(self, text):
        doc = self.nlp(text)
        return doc.vector
    
    def similarity(self, text1, text2):
        doc1 = self.nlp(text1)
        doc2 = self.nlp(text2)
        return doc1.similarity(doc2)
    
    def most_similar(self, word, texts, top_n=5):
        word_vec = self.nlp(word).vector
        similarities = []
        for text in texts:
            text_vec = self.nlp(text).vector
            sim = np.dot(word_vec, text_vec) / (np.linalg.norm(word_vec) * np.linalg.norm(text_vec))
            similarities.append((text, sim))
        
        return sorted(similarities, key=lambda x: x[1], reverse=True)[:top_n]

word_embeddings = WordEmbeddings()
print("WordEmbeddings ready!")'''
nb.cells.append(v4.new_code_cell(code))

# Forecasting
nb.cells.append(v4.new_markdown_cell('### 4. Time Series Forecasting'))
code = '''class TimeSeriesForecaster:
    def __init__(self):
        pass
    
    def forecast(self, df, days=7):
        daily = df.set_index("timestamp").resample("D")["polarity"].mean().dropna()
        
        if len(daily) < 7:
            return {"forecast": [], "confidence": "low"}
        
        # Simple moving average forecast
        recent = daily.tail(7).mean()
        trend = (daily.tail(7).mean() - daily.head(7).mean()) / 7
        
        forecast = []
        for i in range(1, days+1):
            forecast.append({"day": i, "predicted": recent + trend*i, "confidence": 0.6})
        
        return {"forecast": forecast, "trend": "up" if trend > 0 else "down"}
    
    def detect_anomalies(self, df, threshold=2):
        daily = df.set_index("timestamp").resample("D")["polarity"].mean().dropna()
        
        if len(daily) < 5:
            return []
        
        mean = daily.mean()
        std = daily.std()
        
        anomalies = []
        for date, value in daily.items():
            z_score = abs((value - mean) / std) if std > 0 else 0
            if z_score > threshold:
                anomalies.append({"date": date, "value": value, "z_score": z_score})
        
        return anomalies

forecaster = TimeSeriesForecaster()
print("TimeSeriesForecaster ready!")'''
nb.cells.append(v4.new_code_cell(code))

# Save
with open('advanced_nlp.ipynb', 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print('Advanced NLP module created')
