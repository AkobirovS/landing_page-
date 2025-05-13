import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Lead
from .serializers import LeadSerializer

TELEGRAM_BOT_TOKEN = '7810279444:AAH6mmvinNZR3fkSZsPCyPXGtYjnJZkYMiY'
TELEGRAM_CHAT_ID = '6458736545'

@method_decorator(csrf_exempt, name='dispatch')  # отключаем CSRF
class LeadCreateView(APIView):
    def post(self, request):
        serializer = LeadSerializer(data=request.data)
        if serializer.is_valid():
            lead = serializer.save()

            # сообщение для Telegram
            message = (
                f"📥 Новая заявка:\n"
                f"👤 Имя: {lead.first_name}\n"
                f"👤 Фамилия: {lead.last_name}\n"
                f"📞 Телефон: {lead.phone_number}"
            )

            # отправка в Telegram
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                'chat_id': TELEGRAM_CHAT_ID,
                'text': message
            }

            try:
                response = requests.post(url, data=payload)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Ошибка при отправке в Telegram: {e}")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
