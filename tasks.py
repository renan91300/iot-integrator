import json
import pika
import logging
from api.serializers.log import LogSerializer

from celery import shared_task
import paho.mqtt.client as mqtt

@shared_task
def listen_mqtt_topic():      
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("device_logs")
    
    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        # Converte a string para um dicionário
        data = json.loads(msg.payload)
        
        serializer = LogSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logging.info("Log salvo: {}".format(data))

    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    # connect with username and password
    mqttc.username_pw_set("renan", "12345")
    mqttc.connect("localhost", 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    logging.info('Iniciando a escuta do MQTT...')
    mqttc.loop_forever()

