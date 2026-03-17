"""
MindTrace - Sample Data Generator
Generate realistic cognitive pattern data for testing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(n_entries=1000, start_date="2024-01-01"):
    """Generate realistic sample data."""
    
    np.random.seed(42)
    
    texts = {
        "work": [
            "Working on the new project proposal",
            "Code review completed successfully",
            "Meeting with the team about sprint planning",
            "Bug fix released in production",
            "Writing documentation for new feature",
            "Refactoring legacy code",
            "Client call went very well",
            "Preparing quarterly review",
            "Optimizing database queries",
            "Designing new API architecture"
        ],
        "stress": [
            "Feeling overwhelmed with tasks",
            "Stressed about deadline",
            "Cannot focus on anything",
            "Everything is going wrong",
            "Feeling anxious about presentation",
            "Not getting enough sleep",
            "Worried about project timeline",
            "Feeling frustrated",
            "Pressure is building up",
            "Need to take a break"
        ],
        "achievement": [
            "Just finished major milestone",
            "Received great feedback today",
            "Solved complex problem",
            "Productivity at all-time high",
            "Feeling accomplished",
            "Crushed it today",
            "Won team recognition",
            "Completed ahead of schedule",
            "Perfect presentation delivered",
            "Bug fixed before deadline"
        ],
        "personal": [
            "Great dinner with family",
            "Feeling grateful today",
            "Watched wonderful movie",
            "Read amazing book",
            "Spent quality time with friends",
            "Practicing meditation",
            "Started new hobby",
            "Planning weekend trip",
            "Cooked delicious recipe",
            "Journaling about goals"
        ],
        "learning": [
            "Learned new concept",
            "Exploring new framework",
            "Reading research paper",
            "Completed course module",
            "Experimenting with tools",
            "Studying design patterns",
            "Watching tutorial videos",
            "Practicing coding challenges",
            "Following tech blog posts",
            "Attending webinar"
        ],
        "casual": [
            "Just checking in",
            "Random thoughts",
            "Not much happening",
            "Thinking about lunch",
            "Watching TV",
            "Relaxing evening",
            "Browsing social media",
            "Another regular day",
            "Nothing special",
            "Weekend plans"
        ]
    }
    
    start = pd.to_datetime(start_date)
    hour_weights = [0.02, 0.01, 0.01, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.10,
                   0.08, 0.06, 0.07, 0.08, 0.10, 0.08, 0.05, 0.04, 0.03, 0.02,
                   0.02, 0.02, 0.01, 0.01]
    
    data = []
    for _ in range(n_entries):
        hour = np.random.choice(24, p=hour_weights)
        day_offset = np.random.randint(0, 90)
        ts = start + timedelta(days=day_offset, hours=hour, minutes=np.random.randint(0, 60))
        
        if 9 <= hour <= 17:
            cat = np.random.choice(["work", "work", "work", "stress", "achievement", "learning"],
                                  p=[0.30, 0.20, 0.15, 0.15, 0.10, 0.10])
        else:
            cat = np.random.choice(["personal", "casual", "learning"], p=[0.50, 0.30, 0.20])
        
        text = np.random.choice(texts[cat])
        data.append({"timestamp": ts, "text": text})
    
    df = pd.DataFrame(data).sort_values("timestamp").reset_index(drop=True)
    return df

if __name__ == "__main__":
    df = generate_sample_data(500)
    df.to_csv("sample_data.csv", index=False)
    print(f"Generated {len(df)} sample entries")
