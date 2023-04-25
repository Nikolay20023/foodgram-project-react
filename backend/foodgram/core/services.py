from typing import TYPE_CHECKING
from recipes.models import Recipe, RecipeIngredient


if TYPE_CHECKING:
    from recipes.models import Ingredient


def recipe_ingredient_set(
        recipe: Recipe,
        ingredients
) -> None:
    objs = []
    for ingredient, amount in ingredients.values():
        objs.append(
            RecipeIngredient(
                recipe=recipe,
                ingredients=ingredient,
                amount=amount
            )
        )
    RecipeIngredient.objects.bulk_create(objs)


incorrect_layout = str.maketrans(
    'qwertyuiop[]asdfghjkl;\'zxcvbnm,./',
    'йцукенгшщзхъфывапролджэячсмитьбю.'
)