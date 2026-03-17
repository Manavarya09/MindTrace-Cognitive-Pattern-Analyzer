# MindTrace - API Reference

## Classes

### DataIngestion
Data loading and generation module.

**Methods:**
- `load_csv(filepath)` - Load from CSV
- `load_txt(filepath)` - Load from TXT  
- `generate_sample_data(n_entries)` - Generate test data
- `get_data_info()` - Get data summary

### TextPreprocessor
Text cleaning and preprocessing.

**Methods:**
- `clean(text)` - Basic text cleaning
- `remove_stop(text)` - Remove stopwords
- `lemmatize(text)` - Lemmatize words
- `extract_entities(text)` - Named entity recognition
- `process(df)` - Process entire dataframe

### NLPAnalyzer
Sentiment and emotion analysis.

**Methods:**
- `sentiment_vader(text)` - VADER sentiment
- `sentiment_blob(text)` - TextBlob sentiment
- `detect_emotions(text)` - Emotion detection
- `process(df)` - Analyze dataframe

### PatternDetector
Cognitive pattern detection.

**Methods:**
- `add_time_features(df)` - Add time-based features
- `productivity_windows(df)` - Find peak hours
- `behavioral_trends(df)` - Detect trends
- `process(df)` - Run all detection

### TimeSeriesAnalyzer
Time series analysis.

**Methods:**
- `aggregate(df, period)` - Aggregate by period
- `detect_trend(df)` - Detect sentiment trend
- `detect_cycles(df)` - Find recurring patterns
- `process(df)` - Run analysis

### ClusterAnalyzer
Semantic clustering.

**Methods:**
- `create_embeddings(texts)` - Create TF-IDF embeddings
- `cluster(embeddings, n)` - KMeans clustering
- `analyze_clusters(df, labels)` - Analyze clusters
- `reduce_dims(embeddings)` - t-SNE reduction
- `process(df)` - Full clustering

### Visualizer
Interactive Plotly visualizations.

**Methods:**
- `sentiment_timeline(df)` - Timeline chart
- `emotion_bar(df)` - Emotion distribution
- `sentiment_pie(df)` - Sentiment pie chart
- `activity_heatmap(df)` - Activity heatmap
- `clusters_scatter(df)` - Cluster visualization
- `wordcloud(df)` - Word cloud
- `hourly_productivity(df)` - Productivity chart

### InsightGenerator
Automated insight generation.

**Methods:**
- `generate(df, patterns, ts, clusters)` - Generate insights

### ReportGenerator
Cognitive report generation.

**Methods:**
- `generate(df, insights, patterns, clusters, profile)` - Generate report
- `display(df, insights, patterns, clusters, profile)` - Print report

### MindTraceDashboard
Main orchestration class.

**Methods:**
- `run_analysis(n_samples)` - Run full analysis
- `show_visualizations()` - Display charts
- `generate_report()` - Generate report
