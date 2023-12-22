name := "Spark Streaming With Kafka and MongoDB"

version := "1.0"

scalaVersion := "2.12.15"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % "3.2.0",
  "org.apache.spark" %% "spark-sql" % "3.2.0" % "provided",
  "org.mongodb.spark" %% "mongo-spark-connector" % "3.0.1"
)
