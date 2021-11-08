import pika
from .config import *

def publishMessage(message, queue_):
    exchange_ = 'faces_'

    rmq_parameters = pika.URLParameters(f'amqp://{rmq_user}:{rmq_password}@{rmq_host}:{rmq_port}')
    rmq_connection = pika.BlockingConnection(rmq_parameters)
    rmq_channel = rmq_connection.channel()

    rmq_channel.exchange_declare(exchange_)
    rmq_channel.queue_declare(queue=queue_, durable=True)
    rmq_channel.queue_bind(queue_, exchange_, "tests")

    rmq_channel.basic_publish(exchange=exchange_, routing_key="tests", body=message)