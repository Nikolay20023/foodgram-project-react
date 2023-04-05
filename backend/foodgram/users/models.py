from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(max_length=128, unique=True, null=False)

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
        return self.username


class Follow(models.Model):
    class Meta:
        verbose_name = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique_follow'
            )
        ]
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    following = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Подписчик пользлователя'
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} follows {self.following}'
