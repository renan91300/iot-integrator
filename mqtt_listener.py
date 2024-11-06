from datetime import datetime
import json
import logging
import threading
import paho.mqtt.client as mqtt
from api.models.device import DeviceModel
from pymongo import MongoClient

uri = "mongodb://localhost:27017/"
mongoClient = MongoClient(uri)

# display logging on console
logging.basicConfig(level=logging.INFO)

class MqttListener(threading.Thread):
    def __init__(self):
        super().__init__()
        self.client = mqtt.Client(clean_session=False, client_id="dashboard_listener")
        self.client.on_message = self.on_message
        self.running = True

    def connect(self):
        self.client.username_pw_set("renan", "12345")
        self.client.connect(host="localhost", port=1883, keepalive=60)

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload)
        topic = msg.topic
        logging.info(f"ID do dispositivo: {topic.split('/')[1]}")
        logging.info(f"Mensagem recebida no tópico {topic}: {data}")

        device = msg.topic.split('/')[1]
        
        try:
            database = mongoClient.get_database("tcc")
            collection = database.get_collection("received_data")

            collection.insert_one({
                "created_at": datetime.now(),
                "device": device,
                "topic": topic,
                "data": data
            })
        except Exception as e:
            logging.error(f"Erro ao inserir no banco de dados: {e}")
            

    def subscribe_to_devices(self):
        self.client.subscribe("device/+/config")
        devices = DeviceModel.objects.all()
        for device in devices:
            for config in device.received_data_config:
                self.client.subscribe(config.get("topic"))
                logging.info(f"Subscrito no tópico: {config.get('topic' )}")

    def run(self):
        self.connect()
        self.subscribe_to_devices()
        self.client.loop_forever()

    def stop(self):
        self.running = False
        self.client.loop_stop()
        self.client.disconnect()
        logging.info("Cliente MQTT desconectado.")

# Criação do listener quando a aplicação é iniciada
mqtt_listener = MqttListener()
mqtt_listener.start()
