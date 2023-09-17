import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from rest_framework.authentication import get_user_model

load_dotenv()

User = get_user_model()


class Command(BaseCommand):
    help = 'Создание пользователей'

    def handle(self, *args, **options):
        users_data = [
            {
                'username': 'ivan',
                'first_name': 'Ivan',
                'last_name': 'Ivanov',
                'email': 'ivan@example.com',
                'password': os.getenv('DEFAULT_USER_PASSWORD'),
            },
            {
                'username': 'petr',
                'first_name': 'Petr',
                'last_name': 'Petrov',
                'email': 'petr@example.com',
                'password': os.getenv('DEFAULT_USER_PASSWORD'),
            },
            {
                'username': 'sidr',
                'first_name': 'Sidr',
                'last_name': 'Sidorov',
                'email': 'sidr@example.com',
                'password': os.getenv('DEFAULT_USER_PASSWORD'),
            },
        ]

        for user_data in users_data:
            username = user_data['username']
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(**user_data)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Успех! Создан пользователь: {username}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Пользователь {username} уже существует'
                    )
                )
