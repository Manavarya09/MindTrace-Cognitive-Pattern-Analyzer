# MindTrace - Export and Reporting Module

import json
from datetime import datetime

class ResultsExporter:
    def __init__(self):
        pass
    
    def export_json(self, df, results, filepath="mindtrace_results.json"):
        data = {
            "export_date": datetime.now().isoformat(),
            "data_summary": {
                "total_entries": len(df),
                "date_range": f"{df['timestamp'].min()} to {df['timestamp'].max()}"
            },
            "sentiment_summary": {
                "average_polarity": float(df["polarity"].mean()),
                "positive_ratio": float((df["sentiment_label"] == "positive").mean()),
                "negative_ratio": float((df["sentiment_label"] == "negative").mean()),
                "neutral_ratio": float((df["sentiment_label"] == "neutral").mean())
            },
            "emotion_summary": {
                "dominant": df["emotion_dominant"].mode().iloc[0],
                "joy": float(df["emotion_joy"].mean()),
                "sadness": float(df["emotion_sadness"].mean()),
                "fear": float(df["emotion_fear"].mean()),
                "anger": float(df["emotion_anger"].mean())
            },
            "insights": results.get("insights", {}),
            "cluster_profile": results.get("profile", {})
        }
        
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2, default=str)
        
        return filepath
    
    def export_csv_summary(self, df, filepath="mindtrace_summary.csv"):
        daily = df.groupby("date").agg({
            "polarity": "mean",
            "subjectivity": "mean",
            "text": "count"
        }).reset_index()
        daily.columns = ["date", "avg_polarity", "avg_subjectivity", "entry_count"]
        
        daily.to_csv(filepath, index=False)
        return filepath
    
    def export_excel(self, df, filepath="mindtrace_report.xlsx"):
        with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Full Data", index=False)
            
            daily = df.groupby("date").agg({
                "polarity": "mean",
                "emotion_joy": "mean",
                "emotion_sadness": "mean"
            }).reset_index()
            daily.to_excel(writer, sheet_name="Daily Summary", index=False)
        
        return filepath

exporter = ResultsExporter()
print("ResultsExporter ready!")

# Export all
print("Exporting results...")
exporter.export_json(dashboard.df, dashboard.results, "mindtrace_results.json")
exporter.export_csv_summary(dashboard.df, "mindtrace_daily.csv")
print("Export complete!")
