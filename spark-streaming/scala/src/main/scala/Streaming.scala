import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

object Streaming {
  def main(args: Array[String]) = {
    val spark = SparkSession
      .builder()
      .appName("Spark Streaming With Scala and Kafka and MongoDB")
      .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    val df = spark.readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "kafka:9092")
      .option("subscribe", "email-registration-topic")
      .load()

    val rawDF = df.selectExpr("CAST(value AS STRING)").as[String]
    val jsonDF = rawDF.select(from_json($"value", "email STRING, action STRING").as("data"))
                      .select("data.*")

    // Write to MongoDB
    val query = jsonDF.writeStream
                      .outputMode("append")
                      .format("com.mongodb.spark.sql.DefaultSource")
                      .option("uri", "mongodb://mongodb:27017")
                      .option("database", "test_db")
                      .option("collection", "test_collection")
                      .start()

    query.awaitTermination()
  }
}
