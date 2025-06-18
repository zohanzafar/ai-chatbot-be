import os
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from openai import OpenAI
from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatSessionListSerializer


class ChatbotView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        user = request.user
        session_id = request.data.get('session_id', str(uuid.uuid4()))
        session, _ = ChatSession.objects.get_or_create(
            session_id=session_id,
            user=user
        )
        
        user_message = request.data.get('message', '')
        
        ChatMessage.objects.create(
            session=session,
            role='user',
            content=user_message
        )
        
        try:
            chat_history = ChatMessage.objects.filter(session=session).order_by('timestamp')
            
            messages = [
                {"role": msg.role, "content": msg.content} 
                for msg in chat_history
            ]
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            
            assistant_response = response.choices[0].message.content
            
            ChatMessage.objects.create(
                session=session,
                role='assistant',
                content=assistant_response
            )
            
            return Response({
                'session_id': session_id,
                'message': assistant_response
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChatHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id=None):
        if session_id:
            return self.get_single_session(request, session_id)
        return self.get_all_sessions(request)

    def get_all_sessions(self, request):
        try:
            sessions = ChatSession.objects.filter(user=request.user).order_by('-created_at')
            serializer = ChatSessionListSerializer(sessions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Failed to fetch chat sessions: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_single_session(self, request, session_id):
        try:
            session = ChatSession.objects.get(session_id=session_id, user=request.user)
            serializer = ChatSessionSerializer(session)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ChatSession.DoesNotExist:
            return Response(
                {"error": "Chat session not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Error retrieving session: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
