from rest_framework import serializers
from .models import ChatSession, ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['role', 'content', 'timestamp']


class ChatSessionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ['session_id', 'created_at']


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatSession
        fields = ['session_id', 'created_at', 'messages']