from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)
    color = models.CharField(max_length=16)

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=64)
    count = models.IntegerField()
    units = models.CharField(max_length=16)

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    class Meta:
        ordering = ("-name",)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text='Автор',
        related_name='recipes'
    )
    name = models.CharField(max_length=32, blank=False)
    image = models.ImageField(
        'Картинка',
        upload_to='recipe/',
        blank=False
    )
    text = models.CharField(max_length=128, blank=False)
    ingredient = models.OneToOneField(
        Ingredient,
        blank=False,        
        related_name='ingredients',
        on_delete=models.CASCADE
    )
    tag = models.ManyToManyField(
        Tag,
        blank=False,
        through='tags'
    )
    time_to_cooking = models.IntegerField()
    favourite = models.ManyToManyField(
        User,
        related_name='recipe_favourite',
        blank=True
    )

    def __str__(self) -> str:
        return self.name


class UserFollowing(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'following_user_id'], name='unique_follow'
            )
        ]
    user_id = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )
    following_user_id = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
