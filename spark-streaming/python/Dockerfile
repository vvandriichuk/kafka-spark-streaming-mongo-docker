# Используем базовый образ с Java
FROM openjdk:11-jre-slim

# Установка Python и wget
RUN apt-get update && apt-get install -y python3 python3-pip wget && \
    ln -s /usr/bin/python3 /usr/bin/python

# Установка PySpark
RUN pip install pyspark==3.2.0

# Установка Spark
RUN wget https://archive.apache.org/dist/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz && \
    tar xvf spark-3.2.0-bin-hadoop3.2.tgz && \
    mv spark-3.2.0-bin-hadoop3.2 /spark && \
    rm spark-3.2.0-bin-hadoop3.2.tgz

# Скачивание зависимостей для Kafka
RUN wget https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.2.0/spark-sql-kafka-0-10_2.12-3.2.0.jar -P /spark/jars/ && \
    wget https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/2.8.0/kafka-clients-2.8.0.jar -P /spark/jars/ && \
    wget https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.9.0/commons-pool2-2.9.0.jar -P /spark/jars/


# Скачивание дополнительных зависимостей Kafka
RUN wget https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.2.0/spark-token-provider-kafka-0-10_2.12-3.2.0.jar -P /spark/jars/ && \
    wget https://repo1.maven.org/maven2/org/apache/kafka/kafka_2.12/2.8.0/kafka_2.12-2.8.0.jar -P /spark/jars/ && \
    wget https://repo1.maven.org/maven2/org/apache/kafka/kafka-tools/2.8.0/kafka-tools-2.8.0.jar -P /spark/jars/


# Скачивание зависимостей для MongoDB Connector
RUN wget https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.12/3.0.1/mongo-spark-connector_2.12-3.0.1.jar -P /spark/jars/

# Скачивание MongoDB Java Driver
RUN wget https://repo1.maven.org/maven2/org/mongodb/mongo-java-driver/3.12.10/mongo-java-driver-3.12.10.jar -P /spark/jars/


ENV SPARK_HOME=/spark
ENV PATH=$PATH:$SPARK_HOME/bin
ENV PYSPARK_PYTHON=python3

ADD streaming_to_mongo.py /
ADD start_streaming.sh /

RUN chmod +x /start_streaming.sh

CMD ["/start_streaming.sh"]
