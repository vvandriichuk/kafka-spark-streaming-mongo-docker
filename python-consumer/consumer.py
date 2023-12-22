from kafka import KafkaConsumer

consumer = KafkaConsumer("email-registration-topic", bootstrap_servers='kafka:9092', group_id='email-registration-topic-consumer-group')

for msg in consumer:
    print(msg)