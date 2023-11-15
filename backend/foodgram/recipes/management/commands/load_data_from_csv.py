import csv

from django.core.management import BaseCommand

from foodgram.settings import LOAD_DATA_DIR
from recipes.models import Ingredient


class Command(BaseCommand):
    """Служебная команда для загрузки данных в базу из csv."""

    def handle(self, *args, **options):
        with open(
                f'{LOAD_DATA_DIR}/ingredients.csv',
                encoding='utf-8',
        ) as csvfile:
            reader = csv.reader(csvfile)
            ingredient_list = [Ingredient(
                name=row[0],
                measurement_unit=row[1],
            ) for row in reader]
            Ingredient.objects.bulk_create(ingredient_list)
            self.stdout.write(self.style.SUCCESS(
                'Ингредиенты были загружены в базу данных.')
            )
