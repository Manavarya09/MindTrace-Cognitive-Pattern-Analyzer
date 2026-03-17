"""
Prometheus Metrics Exporter for MindTrace
Production-grade monitoring with Prometheus and Grafana
"""
from prometheus_client import Counter, Histogram, Gauge, Summary, CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import start_http_server
from functools import wraps
import time
from typing import Callable


class MindTraceMetrics:
    def __init__(self):
        self.registry = CollectorRegistry()
        
        self.analysis_requests_total = Counter(
            'mindtrace_analysis_requests_total',
            'Total number of analysis requests',
            ['user_id', 'analysis_type'],
            registry=self.registry
        )
        
        self.analysis_duration_seconds = Histogram(
            'mindtrace_analysis_duration_seconds',
            'Time spent on analysis',
            ['analysis_type'],
            buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0],
            registry=self.registry
        )
        
        self.active_users = Gauge(
            'mindtrace_active_users',
            'Number of currently active users',
            registry=self.registry
        )
        
        self.cache_hits_total = Counter(
            'mindtrace_cache_hits_total',
            'Total number of cache hits',
            registry=self.registry
        )
        
        self.cache_misses_total = Counter(
            'mindtrace_cache_misses_total',
            'Total number of cache misses',
            registry=self.registry
        )
        
        self.patterns_detected_total = Counter(
            'mindtrace_patterns_detected_total',
            'Total number of patterns detected',
            ['pattern_type'],
            registry=self.registry
        )
        
        self.sentiment_distribution = Gauge(
            'mindtrace_sentiment_distribution',
            'Sentiment score distribution',
            ['sentiment_category'],
            registry=self.registry
        )
        
        self.queue_size = Gauge(
            'mindtrace_queue_size',
            'Current size of analysis queue',
            registry=self.registry
        )
        
        self.model_inference_seconds = Summary(
            'mindtrace_model_inference_seconds',
            'Model inference time in seconds',
            ['model_name'],
            registry=self.registry
        )
        
        self.error_total = Counter(
            'mindtrace_errors_total',
            'Total number of errors',
            ['error_type'],
            registry=self.registry
        )
    
    def record_analysis(self, user_id: str, analysis_type: str, duration: float):
        self.analysis_requests_total.labels(user_id=user_id, analysis_type=analysis_type).inc()
        self.analysis_duration_seconds.labels(analysis_type=analysis_type).observe(duration)
    
    def record_cache_hit(self):
        self.cache_hits_total.inc()
    
    def record_cache_miss(self):
        self.cache_misses_total.inc()
    
    def record_pattern_detected(self, pattern_type: str):
        self.patterns_detected_total.labels(pattern_type=pattern_type).inc()
    
    def set_active_users(self, count: int):
        self.active_users.set(count)
    
    def set_sentiment_distribution(self, positive: int, neutral: int, negative: int):
        self.sentiment_distribution.labels(sentiment_category='positive').set(positive)
        self.sentiment_distribution.labels(sentiment_category='neutral').set(neutral)
        self.sentiment_distribution.labels(sentiment_category='negative').set(negative)
    
    def set_queue_size(self, size: int):
        self.queue_size.set(size)
    
    def record_error(self, error_type: str):
        self.error_total.labels(error_type=error_type).inc()
    
    def record_model_inference(self, model_name: str, duration: float):
        self.model_inference_seconds.labels(model_name=model_name).observe(duration)
    
    def export_metrics(self) -> bytes:
        return generate_latest(self.registry)


metrics = MindTraceMetrics()


def track_analysis(analysis_type: str):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                metrics.record_analysis(
                    str(kwargs.get('user_id', 'unknown')),
                    analysis_type,
                    duration
                )
                return result
            except Exception as e:
                metrics.record_error(type(e).__name__)
                raise
        return wrapper
    return decorator


def track_model_inference(model_name: str):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                metrics.record_model_inference(model_name, duration)
                return result
            except Exception as e:
                metrics.record_error(f"{model_name}_inference_error")
                raise
        return wrapper
    return decorator


class MetricsExporter:
    def __init__(self, port: int = 9090):
        self.port = port
        self.server = None
    
    def start(self):
        start_http_server(self.port)
        print(f"Metrics server started on port {self.port}")
    
    def stop(self):
        if self.server:
            self.server.shutdown()


if __name__ == "__main__":
    exporter = MetricsExporter()
    exporter.start()
    
    metrics.set_active_users(5)
    metrics.set_sentiment_distribution(30, 50, 20)
    metrics.set_queue_size(10)
    
    print("Prometheus metrics available at http://localhost:9090/metrics")
