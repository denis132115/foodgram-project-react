from django.core.management.base import BaseCommand
import csv
from backend.settings import CSV_FILES_DIR

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импорт ингредиентовЫ'

    def handle(self, *args, **options):
        file_path = f'{CSV_FILES_DIR}/ingredients.csv'

        with open(file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                ingredient_name = row[0].strip()
                ingredient_unit = row[1].strip()

                ingredient, created = Ingredient.objects.get_or_create(
                    name=ingredient_name,
                    unit=ingredient_unit
                )
                self.stdout.write(self.style.SUCCESS(
                    f'Ингредиент добавлен: {ingredient_name}'
                ))
