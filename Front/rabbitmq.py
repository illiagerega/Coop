import pika
import config

queue_ = config.rmq_queue


def receive(type):
    rmq_parameters = pika.URLParameters(f'amqp://{config.rmq_user}:{config.rmq_password}@{config.rmq_host}:{config.rmq_port}')
    rmq_connection = pika.BlockingConnection(rmq_parameters)
    rmq_channel = rmq_connection.channel()


    rmq_channel.queue_declare(queue=type, durable=True)

    method_frame, header_frame, body = rmq_channel.basic_get(queue = type)        
          
    rmq_channel.basic_ack(method_frame.delivery_tag)
    rmq_connection.close() 
    return body