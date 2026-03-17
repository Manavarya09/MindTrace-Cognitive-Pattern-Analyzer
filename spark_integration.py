"""
Apache Spark Integration for Big Data Processing
Distributed computing for MindTrace at scale
"""
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import HashingTF, IDF, Tokenizer, StringIndexer
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier
from pyspark.ml.clustering import LDA, KMeans
from pyspark.ml.evaluation import ClusteringEvaluator, MulticlassClassificationEvaluator
from pyspark.sql.functions import col, udf, window, to_timestamp, expr
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, ArrayType
from pyspark.ml.linalg import Vector, Vectors
from typing import List, Optional
import pandas as pd
import numpy as np


class SparkProcessor:
    def __init__(self, app_name: str = "MindTrace"):
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .config("spark.driver.memory", "4g") \
            .config("spark.executor.memory", "2g") \
            .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
    
    def create_dataframe(self, data: List[dict]) -> "DataFrame":
        schema = StructType([
            StructField("id", StringType(), True),
            StructField("text", StringType(), True),
            StructField("timestamp", StringType(), True),
            StructField("user_id", StringType(), True),
            StructField("category", StringType(), True)
        ])
        return self.spark.createDataFrame(data, schema)
    
    def load_csv(self, path: str, **kwargs) -> "DataFrame":
        return self.spark.read.csv(path, header=True, inferSchema=True, **kwargs)
    
    def load_json(self, path: str) -> "DataFrame":
        return self.spark.read.json(path)
    
    def load_parquet(self, path: str) -> "DataFrame":
        return self.spark.read.parquet(path)
    
    def preprocess_text(self, df: "DataFrame", text_col: str = "text") -> "DataFrame":
        tokenizer = Tokenizer(inputCol=text_col, outputCol="tokens")
        hashingTF = HashingTF(inputCol="tokens", outputCol="rawFeatures", numFeatures=10000)
        idf = IDF(inputCol="rawFeatures", outputCol="features")
        
        pipeline = Pipeline(stages=[tokenizer, hashingTF, idf])
        return pipeline.fit(df).transform(df)
    
    def topic_modeling_lda(self, df: "DataFrame", num_topics: int = 10) -> "DataFrame":
        lda = LDA(k=num_topics, maxIter=10, featuresCol="features")
        return lda.fit(df)
    
    def clustering_kmeans(self, df: "DataFrame", k: int = 5) -> "DataFrame":
        kmeans = KMeans(k=k, featuresCol="features", predictionCol="cluster")
        return kmeans.fit(df).transform(df)
    
    def sentiment_classification(self, df: "DataFrame") -> "DataFrame":
        indexer = StringIndexer(inputCol="sentiment", outputCol="label")
        rf = RandomForestClassifier(featuresCol="features", labelCol="label", numTrees=10)
        
        pipeline = Pipeline(stages=[indexer, rf])
        model = pipeline.fit(df)
        return model.transform(df)
    
    def time_series_aggregation(
        self,
        df: "DataFrame",
        window_duration: str = "1 hour",
        slide_duration: str = "30 minutes"
    ) -> "DataFrame":
        df_ts = df.withColumn("timestamp", to_timestamp(col("timestamp")))
        
        windowed = df_ts.groupBy(
            window(col("timestamp"), window_duration, slide_duration),
            col("user_id")
        ).count()
        
        return windowed.select(
            col("window.start").alias("start"),
            col("window.end").alias("end"),
            col("user_id"),
            col("count")
        )
    
    def distributed_word_count(self, df: "DataFrame", text_col: str = "text") -> "DataFrame":
        words_df = df.select(col(text_col))
        
        import re
        def clean_text(text):
            return re.sub(r'[^\w\s]', '', text.lower())
        
        clean_udf = udf(clean_text)
        
        return words_df \
            .select(expr(f"explode(split({text_col}, ' ')) as word")) \
            .filter(col("word") != "") \
            .groupBy("word") \
            .count() \
            .orderBy(col("count").desc())
    
    def ngram_analysis(self, df: "DataFrame", n: int = 2, top_n: int = 20) -> List[tuple]:
        from pyspark.ml.feature import NGram
        
        tokenizer = Tokenizer(inputCol="text", outputCol="tokens")
        tokens_df = tokenizer.transform(df)
        
        ngram = NGram(n=n, inputCol="tokens", outputCol=f"{n}grams")
        ngram_df = ngram.transform(tokens_df)
        
        return ngram_df.select(f"{n}grams").collect()
    
    def save_parquet(self, df: "DataFrame", path: str, partition_cols: List[str] = None):
        if partition_cols:
            df.write.partitionBy(*partition_cols).parquet(path)
        else:
            df.write.parquet(path)
    
    def stop(self):
        self.spark.stop()


class SparkMLPipeline:
    def __init__(self, spark: SparkSession):
        self.spark = spark
    
    def build_text_classification_pipeline(
        self,
        num_features: int = 10000,
        num_classes: int = 3
    ):
        tokenizer = Tokenizer(inputCol="text", outputCol="tokens")
        hashingTF = HashingTF(inputCol="tokens", outputCol="rawFeatures", numFeatures=num_features)
        idf = IDF(inputCol="rawFeatures", outputCol="features")
        
        lr = LogisticRegression(
            featuresCol="features",
            labelCol="label",
            maxIter=20,
            regParam=0.3
        )
        
        return Pipeline(stages=[tokenizer, hashingTF, idf, lr])
    
    def build_clustering_pipeline(self, num_clusters: int = 5):
        tokenizer = Tokenizer(inputCol="text", outputCol="tokens")
        hashingTF = HashingTF(inputCol="tokens", outputCol="rawFeatures", numFeatures=1000)
        idf = IDF(inputCol="rawFeatures", outputCol="features")
        
        kmeans = KMeans(k=num_clusters, featuresCol="features")
        
        return Pipeline(stages=[tokenizer, hashingTF, idf, kmeans])
    
    def evaluate_clustering(self, predictions: "DataFrame") -> dict:
        evaluator = ClusteringEvaluator(featuresCol="features", predictionCol="prediction")
        silhouette = evaluator.evaluate(predictions)
        
        return {"silhouette_score": silhouette}
    
    def evaluate_classification(self, predictions: "DataFrame") -> dict:
        evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction")
        
        return {
            "accuracy": evaluator.evaluate(predictions, {evaluator.metricName: "accuracy"}),
            "precision": evaluator.evaluate(predictions, {evaluator.metricName: "precisionByNode"}),
            "recall": evaluator.evaluate(predictions, {evaluator.metricName: "recallByNode"}),
            "f1": evaluator.evaluate(predictions, {evaluator.metricName: "f1"})
        }


if __name__ == "__main__":
    processor = SparkProcessor()
    
    sample_data = [
        {"id": "1", "text": "I love working on cognitive analysis", "timestamp": "2024-01-01 10:00:00", "user_id": "1", "category": "work"},
        {"id": "2", "text": "Machine learning is fascinating", "timestamp": "2024-01-01 11:00:00", "user_id": "1", "category": "interest"},
        {"id": "3", "text": "Deep learning patterns emerge over time", "timestamp": "2024-01-01 12:00:00", "user_id": "2", "category": "study"},
    ]
    
    df = processor.create_dataframe(sample_data)
    processed_df = processor.preprocess_text(df)
    
    print("Spark DataFrame created and processed successfully")
    processor.stop()
