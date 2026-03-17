# MindTrace - Testing Module

import unittest
from datetime import datetime

class TestDataIngestion(unittest.TestCase):
    def test_generate_sample_data(self):
        df = ingestion.generate_sample_data(100)
        self.assertEqual(len(df), 100)
        self.assertIn('timestamp', df.columns)
        self.assertIn('text', df.columns)
    
    def test_data_sorted(self):
        df = ingestion.generate_sample_data(50)
        self.assertTrue(df['timestamp'].is_monotonic_increasing)

class TestNLPAnalyzer(unittest.TestCase):
    def test_sentiment_vader(self):
        result = nlp_analyzer.sentiment_vader("This is great!")
        self.assertIn('polarity', result)
        self.assertIn('label', result)
        self.assertGreater(result['polarity'], 0)
    
    def test_sentiment_negative(self):
        result = nlp_analyzer.sentiment_vader("This is terrible!")
        self.assertLess(result['polarity'], 0)

class TestPatternDetector(unittest.TestCase):
    def test_time_features(self):
        df = ingestion.generate_sample_data(50)
        df = pattern_detector.add_time_features(df)
        self.assertIn('hour', df.columns)
        self.assertIn('day_of_week', df.columns)

if __name__ == '__main__':
    unittest.main()
