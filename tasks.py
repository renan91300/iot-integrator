import json
import pika
import logging
from api.serializers.log import LogSerializer

from celery import shared_task
import pika

@shared_task
def listen_mqtt_topic():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='logs', exchange_type='topic')
    channel.queue_declare(queue='device_logs', durable=True)
    channel.queue_bind(exchange='logs', queue='device_logs', routing_key='log.info')
    
    def callback(ch, method, properties, body):
         # Converte o conteúdo binário para uma string
        message = body.decode('utf-8')

        # Converte a string para um dicionário
        data = json.loads(message)
        
        serializer = LogSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logging.info("Log salvo: {}".format(data))

    channel.basic_consume(queue='device_logs', on_message_callback=callback, auto_ack=True)
    
    logging.info('Iniciando a escuta do RabbitMQ...')
    channel.start_consuming()