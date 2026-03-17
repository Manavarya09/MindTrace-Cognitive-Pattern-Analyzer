# MindTrace - Architecture Diagram

## System Architecture

```
+------------------+
|   Data Input    |
|  (CSV, TXT)     |
+--------+---------+
         |
         v
+--------+---------+
| DataIngestion  |
| - load_csv()   |
| - load_txt()   |
| - generate_    |
|   sample()     |
+--------+---------+
         |
         v
+--------+---------+
|TextPreprocessor|
| - clean()      |
| - remove_stop()|
| - lemmatize()  |
| - extract_     |
|   entities()   |
+--------+---------+
         |
         v
+--------+---------+
|  NLPAnalyzer   |
| - sentiment_   |
|   vader()     |
| - sentiment_   |
|   blob()      |
| - detect_     |
|   emotions()  |
+--------+---------+
         |
         v
+--------+---------+
|PatternDetector|
| - add_time_   |
|   features()  |
| - productivity|
|   _windows()  |
| - behavioral_ |
|   trends()    |
+--------+---------+
         |
         v
+--------+---------+
|TimeSeriesAnalyzer|
| - aggregate() |
| - detect_trend()|
| - detect_cycles()|
+--------+---------+
         |
         v
+--------+---------+
|ClusterAnalyzer|
| - create_     |
|   embeddings()|
| - cluster()   |
| - analyze_    |
|   clusters()  |
| - reduce_     |
|   dims()      |
+--------+---------+
         |
         v
+--------+---------+
|  Visualizer   |
| - timeline()  |
| - emotion_bar()|
| - heatmap()   |
| - clusters()  |
| - wordcloud() |
+--------+---------+
         |
         v
+--------+---------+
|InsightGenerator|
| - generate()  |
+--------+---------+
         |
         v
+--------+---------+
|ReportGenerator |
| - generate()  |
| - display()    |
+--------+---------+
         |
         v
+--------+---------+
|    Dashboard   |
| - run_analysis()|
| - show_viz()   |
| - generate_   |
|   report()     |
+--------+---------+
```

## Data Flow
1. Data is loaded from CSV/TXT files
2. Text is preprocessed (clean, lemmatize)
3. NLP analysis performed (sentiment, emotions)
4. Patterns detected (productivity, trends)
5. Time series analysis (trends, cycles)
6. Clustering performed (thinking styles)
7. Visualizations generated
8. Insights generated
9. Report produced
