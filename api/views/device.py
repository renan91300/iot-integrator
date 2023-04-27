from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.models.device import DeviceModel
from api.serializers.device import DeviceSerializer

import pika


class RabbitConnection:
    def send_message(self, topic, message):
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()

        channel.queue_declare(queue=topic)

        channel.basic_publish(exchange="", routing_key=topic, body=message)

        connection.close()

        return True


class DeviceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer
    queryset = DeviceModel.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        RabbitConnection().send_message("hello", "Hello Workd")

        return Response(serializer.data, status=status.HTTP_201_CREATED)
