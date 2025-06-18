from django.urls import path
from .views import ChatbotView, ChatHistoryView

urlpatterns = [
    # Send message
    path('', ChatbotView.as_view(), name='chat'),

    # Get all chats history
    path('chats-history/', ChatHistoryView.as_view(), name='chat_sessions'), 

    # Get a single chat details
    path('chats/<str:session_id>/', ChatHistoryView.as_view(), name='chat_session_detail'),
]
