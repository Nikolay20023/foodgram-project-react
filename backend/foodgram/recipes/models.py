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
        verbose_name='Имя тега',
        unique=True
    )
    slug = models.SlugField(
        max_length=128,
        unique=True,
        verbose_name='Слаг',
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
        ordering = ('name', )

    name = models.CharField(
        max_length=64,
        verbose_name='Имя'
    )
    units = models.CharField(
        max_length=16,
        verbose_name='Единица измерения'
    )

    def __str__(self) -> str:
        return f'{self.name} {self.units}'


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes',
    )
    name = models.CharField(
        max_length=32,
        blank=False,
        verbose_name='Название'
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='media/',
        blank=False
    )
    text = models.CharField(
        max_length=128,
        blank=False,
        verbose_name='Описание',
    )
    pud_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
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

    class Meta:
        ordering = ("-name", )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return f'{self.name}. Автор: {self.author.username}'


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
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites_recipes',
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
        related_name='user_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепты',
        related_name='cart'
    )

    def __str__(self) -> str:
        return f'{self.recipe} в списке покупок:{self.user.username}'
