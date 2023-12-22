from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StringType, StructType, StructField
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

spark = SparkSession \
    .builder \
    .appName("Spark Streaming With Kafka and MongoDB") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0") \
    .getOrCreate()

schema = StructType([
    StructField("email", StringType()),
    StructField("action", StringType())
])

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "email-registration-topic") \
    .option("startingOffsets", "latest") \
    .option("maxOffsetsPerTrigger", 50) \
    .load()

jsonDF = df.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json("json", schema).alias("data")) \
    .select("data.*")

def write_batch_to_mongo(df, epoch_id):
    try:
        logger.info(f"Writing batch {epoch_id} to MongoDB")
        logger.info(f"DataFrame content: {df.collect()}")
        logger.info(f"Number of rows in DataFrame: {df.count()}")
        df.write.format("mongo") \
            .mode("append") \
            .option("uri","mongodb://mongodb:27017") \
            .option("database", "test_db") \
            .option("collection", "test_collection") \
            .save()
        logger.info(f"Successfully wrote batch {epoch_id} to MongoDB")
    except Exception as e:
        logger.error(f"Error writing batch {epoch_id} to MongoDB: {e}", exc_info=True)

query = jsonDF.writeStream \
    .outputMode("append") \
    .trigger(processingTime='10 seconds') \
    .foreachBatch(write_batch_to_mongo) \
    .start()

query.awaitTermination()
