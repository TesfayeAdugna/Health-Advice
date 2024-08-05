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
