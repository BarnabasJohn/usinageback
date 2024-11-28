from rest_framework import serializers
from .models import ManufacturerMessage, ClientMessage


class ClientMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientMessage
        fields = '__all__'


class ManufacturerMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManufacturerMessage
        fields = '__all__'

class CreateConversationSerializer(serializers.Serializer):
    friendly_name = serializers.CharField(max_length=100)

class AddParticipantSerializer(serializers.Serializer):
    conversation_sid = serializers.CharField()
    identity = serializers.CharField()

class SendMessageSerializer(serializers.Serializer):
    conversation_sid = serializers.CharField()
    body = serializers.CharField()
    author = serializers.CharField()