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
