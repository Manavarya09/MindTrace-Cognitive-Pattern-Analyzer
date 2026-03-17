# MindTrace - Batch Processing Module

class BatchProcessor:
    def __init__(self, batch_size=100):
        self.batch_size = batch_size
        self.results = []
    
    def process_in_batches(self, texts, analyzer):
        results = []
        
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i+self.batch_size]
            batch_results = [analyzer.sentiment_vader(t) for t in batch]
            results.extend(batch_results)
            
            if (i + self.batch_size) % 1000 == 0:
                print(f"Processed {i + self.batch_size} entries...")
        
        return results
    
    def parallel_process(self, texts, analyzer, n_jobs=4):
        from sklearn.externals.joblib import Parallel, delayed
        
        results = Parallel(n_jobs=n_jobs)(
            delayed(analyzer.sentiment_vader)(t) for t in texts
        )
        
        return results

batch_processor = BatchProcessor()
print("BatchProcessor ready!")
