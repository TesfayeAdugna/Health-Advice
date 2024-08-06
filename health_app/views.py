from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from health_app.models import AppleHealthStat
from .queries import get_users_with_less_sleep, get_users_with_10000_steps_today, get_users_with_50_percent_less_steps
from .utils import generate_ai_response
# from .serializers import UserSerializer
# from django.contrib.auth import get_user_model


class SleepConditionAPIView(APIView):
    def get(self, request):
        users = get_users_with_less_sleep()
        # users = get_user_model().objects.all()[:1]
        responses = []
        for user in users[:2]:
            data = user.apple_health_stat.all()[:2]
            print(data)
            ai_response = generate_ai_response(user, data)
            responses.append({"user": user.username, "ai_response": ai_response})
        return Response(responses, status=status.HTTP_200_OK)

# class SleepConditionAPIView(APIView):
#     def get(self, request):
#         users = get_users_with_less_sleep()
#         responses = []
#         for user in users:
#             # Extract relevant health statistics data
#             data = user.apple_health_stat.all()
#             formatted_data = [
#                 {
#                     "date": stat.date,  # Assuming 'date' is an attribute of AppleHealthStat
#                     "sleep_hours": stat.sleep_hours,  # Replace with actual attribute names
#                     "steps": stat.steps,
#                     # Add any other relevant fields
#                 }
#                 for stat in data
#             ]
#             ai_response = generate_ai_response(user, formatted_data)
#             responses.append({"user": user.username, "ai_response": ai_response})
#         return Response(responses, status=status.HTTP_200_OK)
    
class Steps1ConditionAPIView(APIView):
    def get(self, request):
        users = get_users_with_10000_steps_today()
        responses = []
        for user in users[:1]:
            data = AppleHealthStat.objects.filter(user=user)[:2]
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
