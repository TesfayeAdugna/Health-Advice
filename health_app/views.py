from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .queries import get_users_with_less_sleep, get_users_with_10000_steps_today, get_users_with_50_percent_less_steps
from .utils import generate_ai_response
from .serializers import UserSerializer

class SleepConditionAPIView(APIView):
    def get(self, request):
        users = get_users_with_less_sleep()
        responses = []
        for user in users:
            data = user.apple_health_stat.all()
            ai_response = generate_ai_response(user, data)
            responses.append({"user": user.username, "ai_response": ai_response})
        return Response(responses, status=status.HTTP_200_OK)

class Steps1ConditionAPIView(APIView):
    def get(self, request):
        users = get_users_with_10000_steps_today()
        responses = []
        for user in users:
            data = user.apple_health_stat.all()
            ai_response = generate_ai_response(user, data)
            responses.append({"user": user.username, "ai_response": ai_response})
        return Response(responses, status=status.HTTP_200_OK)

class Steps2ConditionAPIView(APIView):
    def get(self, request):
        users = get_users_with_50_percent_less_steps()
        responses = []
        for user in users:
            data = user.apple_health_stat.all()
            ai_response = generate_ai_response(user, data)
            responses.append({"user": user.username, "ai_response": ai_response})
        return Response(responses, status=status.HTTP_200_OK)
