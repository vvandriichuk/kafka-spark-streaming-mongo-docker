from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))


counter = 0


def send_email_registration(email):
    message = {'email': email, 'action': 'register'}
    try:
        producer.send('email-registration-topic', value=message)
        producer.flush()
        print(f"Message sent: {message}")
    except Exception as e:
        print(f"Error sending message: {e}")



# Example usage
while True:
    send_email_registration(f'user_{counter}@example.com')
    time.sleep(2)
    counter += 1