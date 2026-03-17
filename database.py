# MindTrace - Database Storage Module

import sqlite3
import json
from datetime import datetime

class Database:
    """SQLite storage for analysis results"""
    
    def __init__(self, db_path="mindtrace.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            text TEXT,
            polarity REAL,
            sentiment TEXT
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS insights (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            insight_type TEXT,
            content TEXT
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY,
            start_time TEXT,
            end_time TEXT,
            entries_count INTEGER
        )''')
        
        conn.commit()
        conn.close()
    
    def save_entry(self, timestamp, text, polarity, sentiment):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO entries VALUES (NULL, ?, ?, ?, ?)",
                 (timestamp, text, polarity, sentiment))
        conn.commit()
        conn.close()
    
    def save_insight(self, insight_type, content):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO insights VALUES (NULL, ?, ?, ?)",
                 (datetime.now(), insight_type, content))
        conn.commit()
        conn.close()
    
    def get_recent_insights(self, limit=10):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM insights ORDER BY id DESC LIMIT ?", (limit,))
        results = c.fetchall()
        conn.close()
        return results

db = Database()
print("Database module ready!")
