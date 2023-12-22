from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StringType, StructType, StructField
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def write_batch_to_file(df, epoch_id):
    """
    Функция для записи данных батча в лог-файл.
    """
    try:
        # Логирование содержимого батча
        logger.info(f"Batch {epoch_id} content:")

        # Запись содержимого батча в файл
        with open("/log/batch_log.txt", "a") as file:
            for row in df.collect():
                file.write(str(row) + "\n")
        logger.info(f"Successfully wrote batch {epoch_id} to file")
    except Exception as e:
        logger.error(f"Error writing batch {epoch_id} to file: {e}", exc_info=True)


def foreach_batch_function(df: DataFrame, epoch_id): # функция для записи батчей
    df.write.mode("append").json("local_log/output_report.json") # датафрейм будет писаться в папку output_report методом append


def main():
    spark = SparkSession \
        .builder \
        .appName("streaming_job") \
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
        .option("startingOffsets", "earliest") \
        .option("maxOffsetsPerTrigger", 50) \
        .load()

    jsonDF = df.selectExpr("CAST(value AS STRING) as json") \
        .select(from_json("json", schema).alias("data")) \
        .select("data.*")

    # пишем на диск
    writer = jsonDF \
        .writeStream \
        .foreachBatch(write_batch_to_file) \
        .trigger(processingTime='10 seconds') \
        .outputMode("append") \
        .start()

    writer.awaitTermination()


main()
