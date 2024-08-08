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
    python manage.py generate_random_users
    python manage.py generate_random_data
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
```
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
├── .env
└── manage.py
```


# Models
## AppleHealthStat
### Model to store Apple Health statistics for users.
```python
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class AppleHealthStat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='apple_health_stat')
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
    created_at = models.DateTimeField()
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
from django.utils import timezone


class Command(BaseCommand):
    help = 'Generate random data for AppleHealthStat'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        users = User.objects.all()
        today = timezone.now().date()

        for user in users:
            for i in range(14):  # Generate data for the last 7 days
                stat = AppleHealthStat(
                    user=user,
                    created_at=today - timedelta(days=i),
                    dateOfBirth=datetime(1980, 1, 1) + timedelta(days=random.randint(0, 365 * 40)),
                    height=random.randint(150, 200),
                    bodyMass=random.randint(50, 100),
                    bodyFatPercentage=random.randint(10, 30),
                    biologicalSex=random.choice(['male', 'female']),
                    activityMoveMode=random.choice(['activeEnergy', 'sedentary']),
                    stepCount=random.uniform(0, 20000),
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
                    sleepAnalysis=[{"date": (datetime.now() - timedelta(days=i)).isoformat(), "sleep_time": random.uniform(0, 1) * 3600} for i in range(12)],
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

from health_app.models import AppleHealthStat

def get_users_with_less_sleep():
    one_week_ago = timezone.now() - timedelta(days=7)
    users = get_user_model().objects.all()
    users_with_less_sleep = []
    
    for user in users:
        total_sleep = 0
        health_stats = AppleHealthStat.objects.filter(user=user, created_at__gte=one_week_ago)
        count = 0
        for stat in health_stats:
            sleep_analyses = stat.sleepAnalysis  # Assuming sleepAnalysis is a list of dictionaries
            total_sleep += sum(sleep['sleep_time'] for sleep in sleep_analyses)
            count += 1

        if total_sleep/7 < 6 * 3600:  # 6 hours in seconds
            users_with_less_sleep.append(user)

    return users_with_less_sleep

def get_users_with_10000_steps_today():
    today = timezone.now().date()
    users = get_user_model().objects.filter(
        apple_health_stat__created_at__date=today,
        apple_health_stat__stepCount__gte = 10000
    ).distinct()

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
    )
    
    filtered_users = users.filter(
        steps_last_week__lt=F('steps_week_before_last') / 2
    )

    return filtered_users
```
# Utilities
## utils.py
### Utility functions including AI response generation.
```python
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')
def generate_ai_response(user, data, topic):
    print(data, "data send to the ai")
    try:

        prompt = f"""
        you are a health assistant providing personalized feedback. Based on the following data, generate a friendly and motivational message for the user.

        
        User: {user.username}
        Data: {data}
        topic: {topic}


        Example Response format:
        "Hello, [name]. I see that you walked [stepCount] steps today, which is 4,000 more than yesterday. It's great that you are so active! I noticed that on days when you walk a lot, you sleep 20% better. Keep it up and continue in the same spirit to reach your goal."
        """
        response = openai.ChatCompletion.create(

            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a health advisor."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"AI generation faild: {str(e)}"

```
## Views
### views.py
API views for handling health conditions.
```python
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
```
### URL Configuration
#### health_app/urls.py
URL routing for the application.
```python
from django.urls import path
from .views import SleepConditionAPIView, Steps1ConditionAPIView, Steps2ConditionAPIView

urlpatterns = [
    path('sleep-condition/', SleepConditionAPIView.as_view(), name='sleep-condition'),
    path('steps1-condition/', Steps1ConditionAPIView.as_view(), name='steps1-condition'),
    path('steps2-condition/', Steps2ConditionAPIView.as_view(), name='steps2-condition'),
    path('absent-users/', AbsentUsersAPIView.as_view(), name='absent-users'),
]
```
