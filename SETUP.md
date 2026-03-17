# MindTrace - Cognitive Pattern Analyzer

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Download NLTK Data
```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('vader_lexicon')
```

### 3. Download spaCy Model
```bash
python -m spacy download en_core_web_sm
```

### 4. Run the Notebook
```bash
jupyter notebook MindTrace.ipynb
```

## Features

- Data Ingestion (CSV, TXT)
- Text Preprocessing
- NLP Analysis (Sentiment, Emotions)
- Pattern Detection
- Time Series Analysis
- Semantic Clustering
- Interactive Visualizations
- Insight Generation

## Usage

1. Open MindTrace.ipynb in Jupyter
2. Run all cells
3. Use sample data or load your own
4. View visualizations and report
