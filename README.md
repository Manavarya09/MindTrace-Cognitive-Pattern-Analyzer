# 🧠 MindTrace — Cognitive Pattern Analyzer

A comprehensive Python-based system that analyzes personal text data (notes, chats, journal entries, or code commits) to extract patterns about thinking style, emotional trends, productivity cycles, and behavioral drift over time.

## 📊 Features

### 1. Data Ingestion
- Load data from **CSV** or **TXT** files
- Each entry must include timestamp and text content

### 2. Text Preprocessing
- Lowercase conversion
- Stopword removal
- Tokenization
- Lemmatization
- Key phrase extraction

### 3. NLP Analysis
- **Sentiment Analysis** - Classifies as positive, neutral, or negative
- **Emotion Detection** - Identifies joy, anger, sadness, fear, surprise, anticipation
- **Topic Modeling** - Uses LDA to discover latent topics

### 4. Cognitive Pattern Detection
- **Productivity Windows** - Identifies peak productivity hours
- **Procrastination Indicators** - Detects negative sentiment + delay patterns
- **Emotional Volatility** - Measures emotional stability over time
- **Behavioral Trends** - Tracks focus vs. distraction patterns

### 5. Time Series Analysis
- Aggregate by day/week/month
- Sentiment trends over time
- Activity frequency analysis
- Cycle detection (peak hours, burnout signals)

### 6. Clustering & Thinking Style
- KMeans clustering on TF-IDF embeddings
- Automatic labeling of thinking styles:
  - 🧠 Deep Work
  - 💭 Casual Thinking
  - 😰 Stress-Driven Writing
  - 🤔 Reflective
  - 📊 Analytical

### 7. Interactive Visualizations (Plotly)
- Sentiment over time (line chart)
- Emotion distribution (bar chart)
- Sentiment breakdown (pie chart)
- Topic clusters (scatter plot)
- Activity heatmap (hour vs day)
- Hourly productivity analysis
- Word cloud

### 8. Insight Generation
- Automated insights like:
  - "You are most productive between 10 AM–12 PM"
  - "Negative sentiment spikes on Mondays"
  - "Focus has decreased over the last 2 weeks"

### 9. Interactive Dashboard (ipywidgets)
- Upload custom files
- Filter by date range
- Toggle visualizations on/off

## 🚀 Getting Started

### Prerequisites

Install required packages:
```bash
pip install pandas numpy matplotlib plotly nltk spacy scikit-learn ipywidgets ipython transformers torch textblob wordcloud nbformat
```

Download NLTK data:
```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
```

Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

### Running the Notebook

1. Open Jupyter Notebook:
```bash
jupyter notebook MindTrace_Cognitive_Pattern_Analyzer.ipynb
```

2. Run the analysis:
```python
# Generate sample data and analyze
dashboard.load_and_analyze(use_sample=True, n_samples=500)

# View visualizations
dashboard.show_visualizations(show_all=True)

# Generate report
dashboard.generate_report()
```

### Loading Your Own Data

**CSV Format:**
```csv
timestamp,text
2024-01-01 10:30:00,Working on the new project proposal
2024-01-01 14:15:00,Had a great lunch with colleagues
```

**TXT Format:**
```
2024-01-01 10:30:00 | Working on the new project proposal
2024-01-01 14:15:00 - Had a great lunch with colleagues
```

**Load your data:**
```python
# Load CSV
df = ingestion.load_csv('your_file.csv', timestamp_col='date', text_col='content')

# Load TXT  
df = ingestion.load_txt('your_file.txt')

# Run analysis
dashboard.df = preprocessor.process_dataframe(df)
dashboard.df = nlp_analyzer.process_dataframe(dashboard.df)
dashboard.df = pattern_detector.process_dataframe(dashboard.df)
```

## 📁 Project Structure

```
MindTrace-Cognitive-Pattern-Analyzer/
├── MindTrace_Cognitive_Pattern_Analyzer.ipynb  # Main notebook
├── sample_data.csv                              # Sample CSV data
├── sample_data.txt                              # Sample TXT data
└── README.md                                    # This file
```

## 🛠️ Technical Details

### Libraries Used
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **matplotlib/seaborn** - Static plotting
- **plotly** - Interactive visualizations
- **nltk** - Natural language processing
- **spaCy** - Advanced NLP
- **scikit-learn** - Machine learning & clustering
- **textblob** - Sentiment analysis
- **transformers** - Advanced NLP (optional)
- **ipywidgets** - Interactive dashboard
- **wordcloud** - Word cloud generation

### Analysis Pipeline
1. Data Loading → 2. Text Preprocessing → 3. NLP Analysis → 4. Pattern Detection → 5. Time Series → 6. Clustering → 7. Visualization → 8. Insights → 9. Report

## 📈 Sample Output

The system generates:
- Summary statistics
- Sentiment trends
- Emotion distributions
- Thinking style clusters
- Activity heatmaps
- Automated insights
- Comprehensive cognitive report

## 🎯 Use Cases

- **Personal Journal Analysis** - Understand emotional patterns
- **Chat Log Analysis** - Discover communication patterns
- **Code Commit Messages** - Track developer productivity
- **Meeting Notes** - Identify topics and sentiment trends
- **Goal Tracking** - Monitor progress and motivation

## 📝 License

MIT License

## 👤 Author

Built with ❤️ for personal development and self-awareness.

---

*Analyze your thoughts. Understand yourself.*
