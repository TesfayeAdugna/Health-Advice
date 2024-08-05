# Health Advice Django Application

## Overview
This Django application is designed to provide personalized health advice to users based on their Apple Health statistics. The application fetches user data, analyzes it, and generates AI-based responses to offer health advice.

## Features
- **Sleep Condition API**: Identifies users with less than 6 hours of sleep on average in the past week and provides personalized advice.
- **Steps Today Condition API**: Identifies users who have walked 10,000 steps today and provides personalized advice.
- **Steps Less Week Condition API**: Identifies users who have walked 50% less this week compared to the previous week and provides personalized advice.

## Setup Instructions

### Prerequisites
- Python 3.x
- Django 5.0.x
- SQLite (default for Django projects)
- OpenAI API Key

### Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd health_advice
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Generate random data:
    ```sh
    python manage.py populate_apple_health_stat
    ```

6. Run the development server:
    ```sh
    python manage.py runserver
    ```

### Environment Variables
Create a `.env` file in the root directory and add your OpenAI API Key:
```makefile
OPENAI_API_KEY=your_openai_api_key```


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

