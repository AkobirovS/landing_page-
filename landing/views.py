import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Lead
from .serializers import LeadSerializer

# Замените на свой настоящий токен и chat_id
TELEGRAM_BOT_TOKEN = 'your_bot_token'
TELEGRAM_CHAT_ID = 'your_chat_id'  # Получить можно через @userinfobot

class LeadCreateView(APIView):
    def get(self, request):
        return Response({"message": "Only POST requests allowed here."})

    def post(self, request):
        serializer = LeadSerializer(data=request.data)
        if serializer.is_valid():
            lead = serializer.save()

            # Отправляем сообщение в Telegram
            message = (
                f"Новая заявка:\n"
                f"Имя: {lead.first_name}\n"
                f"Фамилия: {lead.last_name}\n"
                f"Телефон: {lead.phone_number}"
            )
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                'chat_id': TELEGRAM_CHAT_ID,
                'text': message
            }
            requests.post(url, data=payload)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
