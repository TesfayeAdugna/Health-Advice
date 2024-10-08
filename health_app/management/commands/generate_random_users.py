import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Generate random users for testing'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        num_users = 100 # This number to create more or fewer users
        for i in range(num_users):  
            username = f'user{i}'
            email = f'{username}@example.com'
            password = 'password123'  # password for testing

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

        self.stdout.write(self.style.SUCCESS('Successfully generated random users'))