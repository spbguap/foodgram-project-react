import csv
import os

from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импортируем данные из CSV в БД'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        if not os.path.exists(csv_file_path):
            raise CommandError(f'не найден файл: {csv_file_path}')

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                name = row[0]
                measurement_unit = row[1]

                ingredient, created = Ingredient.objects.get_or_create(
                    name=name, measurement_unit=measurement_unit
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Успех! Импортирован ингредиент: {ingredient}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Ингредиент уже существует: {ingredient}'
                        )
                    )
