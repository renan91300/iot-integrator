import json
import logging
import time

from templated_mail.mail import BaseEmailMessage
from django.conf import settings
from api.serializers.log import LogSerializer

from celery import shared_task, current_task
from celery.exceptions import SoftTimeLimitExceeded
from celery.signals import celeryd_after_setup
from celery.result import AsyncResult
import paho.mqtt.client as mqtt

# @celeryd_after_setup.connect
# def setup_periodic_tasks(sender, **kwargs):
#     listen_mqtt_topic.delay()  # Inicia a escuta assim que o servidor inicializa

# @shared_task(bind=True)
# def listen_mqtt_topic(self):      
#     # The callback for when the client receives a CONNACK response from the server.
#     def on_connect(client, userdata, flags, reason_code, properties):
#         print(f"Connected with result code {reason_code}")
#         # Subscribing in on_connect() means that if we lose the connection and
#         # reconnect then subscriptions will be renewed.
#         client.subscribe("device_logs")
    
#     # The callback for when a PUBLISH message is received from the server.
#     def on_message(client, userdata, msg):
#         # Converte a string para um dicionário
#         data = json.loads(msg.payload)
        
#         #serializer = LogSerializer(data=data)
#         #serializer.is_valid(raise_exception=True)
#         #serializer.save()
#         logging.info("Log salvo: {}".format(data))

#     try:
#         mqttc = mqtt.Client(
#             mqtt.CallbackAPIVersion.VERSION2, 
#             client_id="dashboard_cibele",
#             protocol=mqtt.MQTTv5
#         )
#         mqttc.on_connect = on_connect
#         mqttc.on_message = on_message

#         # connect with username and password
#         mqttc.username_pw_set("renan", "12345")
#         mqttc.connect(
#             host="localhost", 
#             port=1883, 
#             keepalive=60, 
#             clean_start=False)

#         logging.info('Iniciando a escuta do MQTT...')
#         mqttc.loop_start()
#         while True:
#             result = AsyncResult(self.request.id)
#             print(f"Task state: {result.state}")
#             if result.state == 'REVOKED':
#                 logging.info('A task foi revogada. Encerrando a escuta do MQTT...')
#                 break
#             #self.update_state(state='PROGRESS')
#             #current_task.update_state(state='RUNNING')
#             time.sleep(2)
        
#         mqttc.loop_stop()
#         mqttc.disconnect()
#     except SoftTimeLimitExceeded:
#         logging.info('Tempo limite excedido. Encerrando a escuta do MQTT...')
#         mqttc.loop_stop()
#         mqttc.disconnect()

@shared_task
def send_invitation_email(email, token, is_project_invitation=False):
    invite_url = f"{settings.FRONTEND_DOMAIN}/register/{token}/"
    BaseEmailMessage(
        template_name="email/invitation_template.html",
        context={"is_project_invitation": is_project_invitation, "invite_url": invite_url}
    ).send(to=[email])