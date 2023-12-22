FROM python:3.11

ADD consumer.py /
ADD start-consumer.sh /

RUN pip install kafka-python six
RUN chmod +x /start-consumer.sh

CMD ["/start-consumer.sh"]
