# MindTrace - Stream Processing with Kafka

"""
Kafka integration for real-time data streams
"""

KAFKA_AVAILABLE = False

try:
    from kafka import KafkaProducer, KafkaConsumer
    KAFKA_AVAILABLE = True
except:
    pass

class StreamProducer:
    """Publish analysis results to Kafka"""
    
    def __init__(self, bootstrap_servers=['localhost:9092'], topic='mindtrace-results'):
        self.topic = topic
        self.producer = None
        
        if KAFKA_AVAILABLE:
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=bootstrap_servers,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8')
                )
            except:
                self.producer = None
    
    def send(self, data):
        if not self.producer:
            return False
        
        try:
            self.producer.send(self.topic, value=data)
            self.producer.flush()
            return True
        except:
            return False
    
    def close(self):
        if self.producer:
            self.producer.close()

class StreamConsumer:
    """Consume data from Kafka"""
    
    def __init__(self, bootstrap_servers=['localhost:9092'], 
                 topic='mindtrace-input', group_id='mindtrace-group'):
        self.topic = topic
        self.consumer = None
        
        if KAFKA_AVAILABLE:
            try:
                self.consumer = KafkaConsumer(
                    topic,
                    bootstrap_servers=bootstrap_servers,
                    group_id=group_id,
                    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                    auto_offset_reset='earliest'
                )
            except:
                self.consumer = None
    
    def consume(self, timeout_ms=1000):
        if not self.consumer:
            return []
        
        messages = []
        try:
            for message in self.consumer:
                messages.append(message.value)
                if len(messages) >= 100:
                    break
        except:
            pass
        
        return messages
    
    def close(self):
        if self.consumer:
            self.consumer.close()

producer = StreamProducer() if KAFKA_AVAILABLE else None
consumer = StreamConsumer() if KAFKA_AVAILABLE else None
print(f"Kafka integration ready: {KAFKA_AVAILABLE}")
