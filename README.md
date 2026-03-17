# MindTrace Cognitive Pattern Analyzer

## Project Structure

```
MindTrace/
├── MindTrace.ipynb      # Main analysis notebook
├── sample_data.csv      # Sample CSV data
├── sample_data.txt      # Sample TXT data
├── requirements.txt     # Python dependencies
├── SETUP.md            # Setup instructions
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Modules

1. **DataIngestion** - Load CSV, TXT or generate sample data
2. **TextPreprocessor** - Clean, lemmatize, extract entities
3. **NLPAnalyzer** - Sentiment analysis, emotion detection
4. **PatternDetector** - Productivity windows, behavioral trends
5. **TimeSeriesAnalyzer** - Trend detection, cycle analysis
6. **ClusterAnalyzer** - Semantic clustering, thinking styles
7. **Visualizer** - Interactive Plotly charts
8. **InsightGenerator** - Automated insights
9. **ReportGenerator** - Comprehensive reports
10. **MindTraceDashboard** - Main orchestration class

## Features

- Sentiment Analysis (VADER + TextBlob)
- Emotion Detection (Joy, Anger, Sadness, Fear, Surprise, Anticipation)
- Productivity Pattern Detection
- Behavioral Trend Analysis
- Semantic Clustering (KMeans)
- Interactive Visualizations
- Automated Insight Generation

## Sample Data Format

### CSV
```csv
timestamp,text
2024-01-01 10:30:00,Working on project proposal
```

### TXT
```
2024-01-01 10:30:00 | Working on project proposal
```

## Analysis Output

The analysis generates:
- Sentiment timeline with moving averages
- Emotion distribution charts
- Activity heatmaps
- Thinking style clusters
- Word clouds
- Comprehensive cognitive report

## License

MIT License

## Author

MindTrace - Cognitive Pattern Analyzer
