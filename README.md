# Health Advice Django Application

## Overview
This Django application is designed to provide personalized health advice to users based on their Apple Health statistics. The application fetches user data, analyzes it, and generates AI-based responses to offer health advice.

## Features
- **Sleep Condition API**: Identifies users with less than 6 hours of sleep on average in the past week and provides personalized advice.
- **Steps Today Condition API**: Identifies users who have walked 10,000 steps today and provides personalized advice.
- **Steps Less Week Condition API**: Identifies users who have walked 50% less this week compared to the previous week and provides personalized advice.

## Setup Instructions
### Prerequisites
- Python 3.11.5 or higher
- Django 5.0.7 or higher
- SQLite (default for Django projects)
- OpenAI API Key

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/TesfayeAdugna/Health-Advice.git
    cd Health_Advice
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up the database:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

4. Generate random data:
    ```sh
    python manage.py populate_apple_health_stat
    ```

5. Run the development server:
    ```sh
    python manage.py runserver
    ```

### Environment Variables
Create a `.env` file in the root directory and add your OpenAI API Key:
```makefile
OPENAI_API_KEY=your_openai_api_key 
```

# Project Structure

health_advice/
├── health_advice/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── health_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── management/
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── generate_random_data.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py
│   ├── queries.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── db.sqlite3
├── manage.py
└── .env


# Models
## AppleHealthStat
### Model to store Apple Health statistics for users.
```python
from django.db import models
from django.contrib.auth import get_user_model

class AppleHealthStat(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='apple_health_stat')
    dateOfBirth = models.DateTimeField(null=True, blank=True)
    height = models.PositiveSmallIntegerField(null=True, blank=True)
    bodyMass = models.PositiveSmallIntegerField(null=True, blank=True)
    bodyFatPercentage = models.PositiveSmallIntegerField(null=True, blank=True)
    biologicalSex = models.CharField(max_length=32, null=True, blank=True)
    activityMoveMode = models.CharField(max_length=128, null=True, blank=True)
    stepCount = models.PositiveSmallIntegerField(null=True, blank=True)
    basalEnergyBurned = models.PositiveSmallIntegerField(null=True, blank=True)
    activeEnergyBurned = models.PositiveSmallIntegerField(null=True, blank=True)
    flightsClimbed = models.PositiveSmallIntegerField(null=True, blank=True)
    appleExerciseTime = models.PositiveSmallIntegerField(null=True, blank=True)
    appleMoveTime = models.PositiveSmallIntegerField(null=True, blank=True)
    appleStandHour = models.PositiveSmallIntegerField(null=True, blank=True)
    menstrualFlow = models.CharField(max_length=128, null=True, blank=True)
    HKWorkoutTypeIdentifier = models.CharField(max_length=128, null=True, blank=True)
    heartRate = models.PositiveSmallIntegerField(null=True, blank=True)
    oxygenSaturation = models.PositiveSmallIntegerField(null=True, blank=True)
    mindfulSession = models.JSONField(null=True, blank=True)
    sleepAnalysis = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```
# Management Command
## generate_random_data.py
### Command to generate random Apple Health data for users.
```python
import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from health_app.models import AppleHealthStat
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generate random data for AppleHealthStat'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        users = User.objects.all()

        for user in users:
            for _ in range(30):  # Generate data for the last 30 days
                stat = AppleHealthStat(
                    user=user,
                    dateOfBirth=datetime(1980, 1, 1) + timedelta(days=random.randint(0, 365 * 40)),
                    height=random.randint(150, 200),
                    bodyMass=random.randint(50, 100),
                    bodyFatPercentage=random.randint(10, 30),
                    biologicalSex=random.choice(['male', 'female']),
                    activityMoveMode=random.choice(['activeEnergy', 'sedentary']),
                    stepCount=random.randint(0, 20000),
                    basalEnergyBurned=random.randint(1000, 3000),
                    activeEnergyBurned=random.randint(100, 1000),
                    flightsClimbed=random.randint(0, 20),
                    appleExerciseTime=random.randint(0, 120),
                    appleMoveTime=random.randint(0, 120),
                    appleStandHour=random.randint(0, 24),
                    menstrualFlow=random.choice(['unspecified', 'light', 'medium', 'heavy']),
                    HKWorkoutTypeIdentifier=random.choice(['running', 'walking', 'cycling']),
                    heartRate=random.randint(60, 100),
                    oxygenSaturation=random.randint(95, 100),
                    mindfulSession={"sessions": [random.randint(0, 60) for _ in range(7)]},
                    sleepAnalysis=[{"date": (datetime.now() - timedelta(days=i)).isoformat(), "sleep_time": random.uniform(0, 8) * 3600} for i in range(7)],
                )
                stat.save()

        self.stdout.write(self.style.SUCCESS('Successfully generated random data'))
```

# Queries
## queries.py
### Contains functions to fetch users based on specific conditions.
```python
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Q, F
from django.contrib.auth import get_user_model

def get_users_with_less_sleep():
    one_week_ago = timezone.now() - timedelta(days=7)
    users = get_user_model().objects.filter(
        apple_health_stat__created_at__gte=one_week_ago
    ).annotate(
        total_sleep=Sum('apple_health_stat__sleepAnalysis__sleep_time')
    ).filter(total_sleep__lt=6*3600)  # 6 hours in seconds
    return users

def get_users_with_10000_steps_today():
    today = timezone.now().date()
    users = get_user_model().objects.filter(
        apple_health_stat__created_at__date=today,
        apple_health_stat__stepCount__gte=10000
    )
    return users

def get_users_with_50_percent_less_steps():
    today = timezone.now().date()
    one_week_ago = today - timedelta(days=7)
    two_weeks_ago = today - timedelta(days=14)

    users = get_user_model().objects.annotate(
        steps_last_week=Sum(
            'apple_health_stat__stepCount',
            filter=Q(apple_health_stat__created_at__date__gte=one_week_ago)
        ),
        steps_week_before_last=Sum(
            'apple_health_stat__stepCount',
            filter=Q(apple_health_stat__created_at__date__gte=two_weeks_ago) & Q(apple_health_stat__created_at__date__lt=one_week_ago)
        )
    ).filter(
        steps_last_week__lt=F('steps_week_before_last') / 2
    )
    return users
```
# Utilities
## utils.py
### Utility functions including AI response generation.
```python
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def generate_ai_response(user, data):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a health advisor."},
            {"role": "user", "content": f"Hello, {user.username}. Here is your health data: {data}. Can you provide some personalized advice and analysis?"}
        ]
    )
    return response.choices[0].message['content']
```
## Views
### views.py
API views for handling health conditions.
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .queries import get_users_with_less_sleep, get_users_with_10000_steps_today, get_users_with_50_percent_less_steps
from .utils import generate_ai_response
from .serializers import UserSerializer

class SleepConditionAPI(APIView):
    def get(self, request, *args, **kwargs):
        users = get_users_with_less_sleep()
        data = [UserSerializer(user).data for user in users]
        response_data = [{"user": user_data, "advice": generate_ai_response(user_data, "sleep")} for user_data in data]
        return Response(response_data, status=status.HTTP_200_OK)

class StepsTodayConditionAPI(APIView):
    def get(self, request, *args, **kwargs):
        users = get_users_with_10000_steps_today()
        data = [UserSerializer(user).data for user in users]
        response_data = [{"user": user_data, "advice": generate_ai_response(user_data, "steps_today")} for user_data in data]
        return Response(response_data, status=status.HTTP_200_OK)

class StepsLessWeekConditionAPI(APIView):
    def get(self, request, *args, **kwargs):
        users = get_users_with_50_percent_less_steps()
        data = [UserSerializer(user).data for user in users]
        response_data = [{"user": user_data, "advice": generate_ai_response(user_data, "steps_less_week")} for user_data in data]
        return Response(response_data, status=status.HTTP_200_OK)
```
# Serializers
## serializers.py
### Serializer for user data.
```python
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import AppleHealthStat

class AppleHealthStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppleHealthStat
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    apple_health_stat = AppleHealthStatSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'apple_health_stat']
```
# URL Configuration
## urls.py
### URL routing for the application.
```python
from django.contrib import admin
from django.urls import path, include
from health_app.views import SleepConditionAPI, StepsTodayConditionAPI, StepsLessWeekConditionAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/sleep-condition/', SleepConditionAPI.as_view(), name='sleep-condition'),
    path('api/steps-today-condition/', StepsTodayConditionAPI.as_view(), name='steps-today-condition'),
    path('api/steps-less-week-condition/', StepsLessWeekConditionAPI.as_view(), name='steps-less-week-condition'),
]
```
