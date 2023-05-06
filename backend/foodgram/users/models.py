from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(max_length=128, unique=True, null=False)
    is_active = models.BooleanField(
        verbose_name='Активирован',
        default=True
    )

    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name'
    ]
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        ordering = ['id']

    def __str__(self):
        return f'{self.username}: {self.email}'


class Follow(models.Model):
    """
    Attributes:
        author(int):
            Автор рецепта. Связь через ForeignKey.
        user(int):
            Подписчик Связь через ForeignKey.
        date_added(datetime):
            Дата создания подписки.
    """
    class Meta:
        verbose_name = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follow'
            )
        ]
    user = models.ForeignKey(
        User,
        related_name='subscriptions',
        on_delete=models.CASCADE,
        verbose_name='Подписчик пользлователя'
    )
    author = models.ForeignKey(
        User,
        related_name='subscribers',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} -> {self.user}'
