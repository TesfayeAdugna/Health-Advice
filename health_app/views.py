from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from health_app.models import AppleHealthStat
from .queries import get_absent_users, get_users_with_less_sleep, get_users_with_10000_steps_today, get_users_with_50_percent_less_steps
from .utils import generate_ai_response
from django.core.serializers import serialize
import json
from django.contrib.auth import get_user_model
from django.db.models import Sum


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
    

class AbsentUsersAPIView(APIView):
    def get(self, request):
        absent_users = get_absent_users()
        responses = []

        for username, days_absent in absent_users.items():
            if days_absent == 0 or days_absent % 30 != 0: continue

            user = get_user_model().objects.get(username=username)
            data = AppleHealthStat.objects.filter(user=user)
            
            # Summing up the total steps, calories burned, and perfect sleep nights
            total_steps = data.aggregate(Sum('stepCount'))['stepCount__sum'] or 0
            total_calories = data.aggregate(Sum('activeEnergyBurned'))['activeEnergyBurned__sum'] or 0
            perfect_sleep_nights = sum(
                1 for stat in data if stat.sleepAnalysis[0]['sleep_time'] >= 8 * 3600
            )

            # Generate the message
            message = (
                f"It’s been {days_absent} days since we last saw you. During this period that you were with us "
                f"you walked more than {total_steps} steps, burned {total_calories} calories and had "
                f"{perfect_sleep_nights} nights of perfect sleep. Your wellness journey is important to us, "
                f"continue the path to self-improvement in Hapday. Let’s catch up!"
            )
            
            responses.append({
                "user": user.username,
                "message": message
            })

        return Response(responses, status=status.HTTP_200_OK)
