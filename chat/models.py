from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class ChatSession(models.Model):
    """
    Represents a chat session with unique identifier
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Session {self.session_id}"


class ChatMessage(models.Model):
    """
    Stores individual chat messages
    """
    SESSION_ROLES = (
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System')
    )
    
    session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=SESSION_ROLES)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}"