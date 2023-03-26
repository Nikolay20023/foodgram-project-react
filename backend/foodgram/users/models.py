from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    GUEST = 'guest'
    AUTHORIZED = 'authorized_user'
    ADMIN = 'admin'

    USER_ROLE = (
        (GUEST, 'guest'),
        (AUTHORIZED, 'authorized_user'),
        (ADMIN, 'admin')
    )
    role = models.CharField(
        'Роль',
        max_length=30,
        choices=USER_ROLE,
        default=GUEST
    )

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (
            self.role == User.ADMIN
            or self.is_superuser
        )


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
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    following_user_id = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE,
        verbose_name='Подписчик пользлователя'
    )
    created = models.DateTimeField(auto_now_add=True)
