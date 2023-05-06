from recipes.models import Recipe, RecipeIngredient


def recipe_ingredients_set(
    recipe: Recipe,
    ingredients
) -> None:
    """Записывает ингредиенты вложенные в рецепт.
    Создаёт объект AmountIngredient связывающий объекты Recipe и
    Ingredient с указанием количества(`amount`) конкретного ингридиента.
    Args:
        recipe (Recipe):
            Рецепт, в который нужно добавить игридиенты.
        ingridients (list[dict]):
            Список ингридентов и количества сих.
    """
    objs = []

    for ingredient, amount in ingredients.values():
        objs.append(RecipeIngredient(
            recipe=recipe,
            ingredient=ingredient,
            amount=amount
        ))

    RecipeIngredient.objects.bulk_create(objs)


incorrect_layout = str.maketrans(
    'qwertyuiop[]asdfghjkl;\'zxcvbnm,./',
    'йцукенгшщзхъфывапролджэячсмитьбю.'
)
