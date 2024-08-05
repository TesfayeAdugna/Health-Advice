import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Generate random users for testing'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        for _ in range(10):  # Change this number to create more or fewer users
            username = f'user{random.randint(1, 1000)}'
            email = f'{username}@example.com'
            password = 'password123'  # Use a simple password for testing

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

        self.stdout.write(self.style.SUCCESS('Successfully generated random users'))