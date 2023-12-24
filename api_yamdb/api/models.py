from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER)
    verification_code = models.CharField(max_length=4)
