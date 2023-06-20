from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.models.device import DeviceModel
from api.serializers.device import DeviceSerializer, DeviceDetailsSerializer
from api.serializers.device_academics import DeviceAcademicsSerializer

import pika
import json


class RabbitConnection:
    def send_message(self, topic, message):
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()

        channel.queue_delete(queue=topic)
        channel.queue_declare(queue=topic)

        channel.basic_publish(exchange="", routing_key=topic, body=message)

        connection.close()

        return True


class DeviceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = DeviceModel.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ["retrieve"]:
            return DeviceDetailsSerializer
        return DeviceSerializer
    
    def create(self, request, *args, **kwargs):
        data = request.data
        academics_data = data.pop("academics", [])
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                device_instance = serializer.save()

                academics_data = [academic|{"device": device_instance.id} for academic in academics_data]
                device_academics_serializer = DeviceAcademicsSerializer(data=academics_data, many=True)
                try:
                    device_academics_serializer.is_valid(raise_exception=True)
                    device_academics_instances = device_academics_serializer.save()
                except ValidationError as exc:
                        errors = exc.get_full_details()
                        self.perform_destroy(device_instance)
                        raise ValidationError(errors)

                rabbit_allowed_tags = [
                    {
                        "hash": instance.academic.key,
                        "access_period": instance.access_period
                    } 
                    for instance in device_academics_instances
                ]
                
                rabbit_topic_data = {"settings": device_instance.settings, "allowed_tags": rabbit_allowed_tags}

                RabbitConnection().send_message(device_instance.name, json.dumps(rabbit_topic_data))

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({"erro": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        data = request.data
        academics_data = data.pop("academics", [])
        
        device_instance = get_object_or_404(DeviceModel, id=kwargs["pk"])
        serializer = DeviceSerializer(device_instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()


        academics_data = [academic|{"device": device_instance.id} for academic in academics_data]
        device_academics_serializer = DeviceAcademicsSerializer(data=academics_data, many=True)
        try:
            device_academics_serializer.is_valid(raise_exception=True)
            device_instance.academics.clear()
            device_academics_instances = device_academics_serializer.save()
        except ValidationError as exc:
                errors = exc.get_full_details()
                raise ValidationError(errors)

        rabbit_allowed_tags = [
            {
                "hash": instance.academic.key,
                "access_period": instance.access_period
            } 
            for instance in device_academics_instances
        ]

        rabbit_topic_data = {"settings": data["settings"], "allowed_tags": rabbit_allowed_tags}

        RabbitConnection().send_message(data["name"], json.dumps(rabbit_topic_data))

        return Response("ok")