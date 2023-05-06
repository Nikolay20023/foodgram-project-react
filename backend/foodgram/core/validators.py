from django.core.exceptions import ValidationError


def ingredients_validator(
    ingredients,
    Ingredient,
) -> dict:
    """Проверяет список ингридиентов.
    Args:
        ingredients (list[dict[str, str | int]]):
            Список ингридиентов.
            Example: [{'amount': '5', 'id': 2073},]
        Ingredient (Ingredient):
            Модель ингридиентов во избежании цикличного импорта.
    Raises:
        ValidationError: Ошибка в переданном списке ингридиентов.
    Returns:
        dict[int, tuple[Ingredient, int]]:
    """

    valid_ings = {}

    for ing in ingredients:
        if not (isinstance(ing['amount'], int) or ing['amount'].isdigit()):
            raise ValidationError('Неправильное количество ингидиента')

        amount = valid_ings.get(ing['id'], 0) + int(ing['amount'])
        if amount <= 0:
            raise ValidationError('Неправильное количество ингидиента')

        valid_ings[ing['id']] = amount

    if not valid_ings:
        raise ValidationError('Неправильные ингредиенты')
    db_ings = Ingredient.objects.filter(pk__in=valid_ings.keys())
    if not db_ings:
        raise ValidationError('Неправильные ингредиенты')

    for ing in db_ings:
        valid_ings[ing.pk] = (ing, valid_ings[ing.pk])

    return valid_ings


def tags_exist_validators(tags_ids, Tag):

    exists_tags = Tag.objects.filter(id__in=tags_ids)
    if len(exists_tags) != len(tags_ids):
        raise ValidationError(
            f'указан несуществующий тег {tags_ids}, {exists_tags}'
        )
