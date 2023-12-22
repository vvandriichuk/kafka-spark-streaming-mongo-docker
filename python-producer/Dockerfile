FROM python:3.11

ADD producer.py /
ADD start-producer.sh /

RUN pip install kafka-python six
RUN chmod +x /start-producer.sh

CMD ["/start-producer.sh"]
