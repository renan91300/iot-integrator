from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from api.models.device import DeviceModel
from api.serializers.device import DeviceSerializer, PostDeviceSerializer
from mqtt_listener import mqtt_listener

import paho.mqtt.publish as publish
import json
from pymongo import MongoClient


class MqttConnection:
    def send_message(self, topic, message):
        try:
            publish.single(
                topic,
                message,
                hostname="localhost",
                port=1883,
                auth={"username": "renan", "password": "12345"},
            )
        except Exception as e:
            print(f"Error: {e}")
            return False

        return True


class DeviceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = DeviceModel.objects.all()
    serializer_class = DeviceSerializer

    def get_queryset(self):
        project_id = self.request.GET.get("project_id")
        queryset = self.queryset.filter(
            project=project_id, project__members=self.request.user.id
        )
        return queryset

    def create(self, request, *args, **kwargs):
        project = request.GET.get("project_id")
        if not project:
            return Response(
                "É necessário informar o projeto", status=status.HTTP_400_BAD_REQUEST
            )
        data = request.data
        data["project"] = project
        data["location"] = data["location"]["id"]
        data["category"] = data["category"]["id"]
        
        try:
            with transaction.atomic():
                serializer = PostDeviceSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                device_instance = serializer.save()

                mqtt_config_topic = f"device/{device_instance.id}/config"
                mqtt_message = json.dumps(
                    {
                        "status": device_instance.status,
                        "configs": device_instance.config,
                    }
                )
                MqttConnection().send_message(mqtt_config_topic, mqtt_message)

                mqtt_listener.subscribe_to_devices()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({"erro": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = request.data

        device_instance = get_object_or_404(DeviceModel, id=kwargs["pk"])
        serializer = DeviceSerializer(device_instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer = serializer.data

        mqtt_config_topic = f"device/{kwargs['pk']}/config"
        mqtt_message = json.dumps(
            {"status": serializer["status"], "configs": serializer["config"]}
        )
        
        MqttConnection().send_message(mqtt_config_topic, mqtt_message)

        return Response("ok")

    @action(detail=True, methods=["get"])
    def get_device_data(self, request, *args, **kwargs):
        device = self.get_object()

        client = MongoClient("mongodb://localhost:27017/")
        db = client["tcc"]  # Substitua pelo nome do banco
        collection = db["received_data"]  # Substitua pelo nome da coleção

        data = {}
        for field in device.received_data_config:
            # Busca os dados no mongo
            data[field["name"]] = list(
                collection.find(
                    {"device": str(device.id), "topic": field["topic"]},
                    {"_id": 0, "created_at": 1, f"data": 1},
                ).sort("created_at", -1).limit(100)
            )

        return Response(data)
