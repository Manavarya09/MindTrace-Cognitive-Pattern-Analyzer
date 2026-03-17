# MindTrace - Example Usage

## Basic Usage

```python
# Import dashboard
from MindTrace import MindTraceDashboard

# Create dashboard
dashboard = MindTraceDashboard()

# Run analysis with sample data
dashboard.run_analysis(n_samples=1000)

# Show visualizations
dashboard.show_visualizations()

# Generate report
dashboard.generate_report()
```

## Load Your Own Data

```python
# From CSV
df = ingestion.load_csv('your_data.csv')

# From TXT
df = ingestion.load_txt('your_data.txt')

# Preprocess
df = preprocessor.process(df)

# Analyze
df = nlp_analyzer.process(df)
df, patterns = pattern_detector.process(df)
```

## Custom Analysis

```python
# Get specific insights
insights = insight_generator.generate(df, patterns, ts_results, cluster_profile)

# Create specific visualization
fig = visualizer.sentiment_timeline(df)
fig.show()

# Generate report
report = report_generator.generate(df, insights, patterns, clusters, profile)
```

## Configuration

```python
# Adjust clustering
df, clusters, profile = cluster_analyzer.process(df, n_clusters=5)

# Change time period
daily = ts_analyzer.aggregate(df, period='W')  # Weekly
```

## Output

The analyzer generates:
- Sentiment analysis (polarity, subjectivity, labels)
- Emotion scores (joy, anger, sadness, fear, surprise, anticipation)
- Time features (hour, day, week, month)
- Productivity scores
- Focus scores
- Behavioral trends
- Cluster assignments
- t-SNE coordinates for visualization
