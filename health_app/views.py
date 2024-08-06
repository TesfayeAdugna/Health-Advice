from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from health_app.models import AppleHealthStat
from .queries import get_users_with_less_sleep, get_users_with_10000_steps_today, get_users_with_50_percent_less_steps
from .utils import generate_ai_response
from django.core.serializers import serialize
import json
from django.contrib.auth import get_user_model


class SleepConditionAPIView(APIView):
    def get(self, request):
        users = get_users_with_less_sleep()
        responses = []
        for user in users:
            datas = AppleHealthStat.objects.filter(user=user)
            
            json_data = serialize('json', datas)

            ai_response = generate_ai_response(user, json_data, "Users with a week of sleep less than 6 hours.")
            responses.append({"user": user.username, "ai_response": ai_response})
        
        return Response(responses, status=status.HTTP_200_OK)

class Steps1ConditionAPIView(APIView):
    def get(self, request):
        users = get_users_with_10000_steps_today()
        responses = []
        for user in users:
            data = AppleHealthStat.objects.filter(user=user)
            ai_response = generate_ai_response(user, data, "Users who have reached 10,000 steps today.")
            responses.append({"user": user.username, "ai_response": ai_response})
        return Response(responses, status=status.HTTP_200_OK)

class Steps2ConditionAPIView(APIView):
    def get(self, request):
        users = get_users_with_50_percent_less_steps()
        responses = []
        for user in users:
            data = user.apple_health_stat.all()
            ai_response = generate_ai_response(user, data, "Users who walked 50%\ less this week compared to the previous week.")
            responses.append({"user": user.username, "ai_response": ai_response})
        return Response(responses, status=status.HTTP_200_OK)
