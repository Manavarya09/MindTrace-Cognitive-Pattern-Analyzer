# MindTrace - Metrics and Statistics Module

class MetricsCalculator:
    def __init__(self):
        pass
    
    def calculate_all(self, df):
        return {
            "entry_metrics": {
                "total": len(df),
                "unique_days": df["timestamp"].dt.date.nunique(),
                "avg_per_day": len(df) / df["timestamp"].dt.date.nunique()
            },
            "sentiment_metrics": {
                "mean_polarity": float(df["polarity"].mean()),
                "median_polarity": float(df["polarity"].median()),
                "std_polarity": float(df["polarity"].std()),
                "positive_ratio": float((df["sentiment_label"] == "positive").mean()),
                "negative_ratio": float((df["sentiment_label"] == "negative").mean())
            },
            "emotion_metrics": {
                "dominant_emotion": df["emotion_dominant"].mode().iloc[0],
                "joy_avg": float(df["emotion_joy"].mean()),
                "sadness_avg": float(df["emotion_sadness"].mean()),
                "fear_avg": float(df["emotion_fear"].mean()),
                "anger_avg": float(df["emotion_anger"].mean())
            },
            "temporal_metrics": {
                "most_active_hour": int(df["hour"].mode().iloc[0]),
                "most_active_day": df["day_name"].mode().iloc[0],
                "weekend_ratio": float(df["is_weekend"].mean())
            },
            "text_metrics": {
                "avg_word_count": float(df["text"].str.split().str.len().mean()),
                "total_words": int(df["text"].str.split().str.len().sum())
            }
        }

metrics_calc = MetricsCalculator()
print("MetricsCalculator ready!")
