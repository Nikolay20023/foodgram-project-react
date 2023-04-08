import json

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):

    def add_arguments(self, parser) -> None:
        parser.add_argument('json_file', type=str)

    def handle(self, *args, **options):
        json_file = options['json_file']
        Ingredient.objects.all().delete()

        with open(json_file, encoding='utf-8') as f:
            data = json.load(f)
        for ingredient in data:
            Ingredient.objects.create(
                name=ingredient['name'],
                units=ingredient['measurement_unit']
            )
