# MindTrace - Data Validation Module

import pandas as pd

class DataValidator:
    def __init__(self):
        self.errors = []
    
    def validate_timestamp(self, df):
        if 'timestamp' not in df.columns:
            self.errors.append("Missing timestamp column")
            return False
        
        if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
            self.errors.append("Timestamp column must be datetime type")
            return False
        
        return True
    
    def validate_text(self, df):
        if 'text' not in df.columns:
            self.errors.append("Missing text column")
            return False
        
        null_count = df['text'].isnull().sum()
        if null_count > 0:
            self.errors.append(f"Found {null_count} null text entries")
            return False
        
        empty_count = (df['text'] == '').sum()
        if empty_count > 0:
            self.errors.append(f"Found {empty_count} empty text entries")
            return False
        
        return True
    
    def validate_all(self, df):
        self.errors = []
        
        timestamp_ok = self.validate_timestamp(df)
        text_ok = self.validate_text(df)
        
        if self.errors:
            return False, self.errors
        
        return True, []
    
    def get_summary(self, df):
        return {
            "total_entries": len(df),
            "date_range": f"{df['timestamp'].min()} to {df['timestamp'].max()}",
            "text_stats": {
                "min_length": df['text'].str.len().min(),
                "max_length": df['text'].str.len().max(),
                "avg_length": df['text'].str.len().mean()
            }
        }

validator = DataValidator()
print("DataValidator ready!")
