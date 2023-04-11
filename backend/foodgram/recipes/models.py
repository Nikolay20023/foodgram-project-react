from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class Tag(models.Model):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    name = models.CharField(
        max_length=128,
        verbose_name='Имя тега'
    )
    slug = models.SlugField(
        max_length=128,
        unique=True,
        verbose_name='Слаг'
    )
    color = models.CharField(
        max_length=16,
        verbose_name='Цвет 000x'
    )

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    name = models.CharField(
        max_length=64,
        verbose_name='Имя'
    )
    units = models.CharField(
        max_length=16,
        verbose_name='Единица измерения'
    )

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    class Meta:
        ordering = ("-name",)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes'
    )
    name = models.CharField(
        max_length=32,
        blank=False,
        verbose_name='Название'
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipe/',
        blank=False
    )
    text = models.CharField(
        max_length=128,
        blank=False,
        verbose_name='Описание',
    )
    ingredient = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты'
    )
    tag = models.ManyToManyField(
        Tag,
        blank=False,
        verbose_name='Теги'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(
                1,
                message='Минимальное время приготовление 1 минута'
            )
        ]
    )

    def __str__(self) -> str:
        return self.name


class Favourite(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favourite_usr_recipe'
            )
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='users'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Рецепты',
    )


class RecipeIngredient(models.Model):
    class Meta:
        verbose_name = 'Ингредиент_в_рецепте'
        verbose_name_plural = 'Ингредиенты_в_рецепте'
        constraints = [
            models.UniqueConstraint(fields=('ingredient', 'recipe'),
                                    name='unique_recipes_ingredient')
        ]

    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=(
            MinValueValidator(
                1, message='Минимальное количество ингредиентов 1'
            ),
        )
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиенты',
        related_name='ingredient_recipes'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_ingredients'
    )

    def __str__(self) -> str:
        return f'{self.ingredient} в {self.recipe}'


class ShoppingCart(models.Model):
    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(fields=('user', 'recipe'),
                                    name='unique_cart_user')
        ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепты',
    )

    def __str__(self) -> str:
        return f'{self.recipe} в списке покупок пользователя:{self.user}'
