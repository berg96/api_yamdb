from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import correct_year, validate_username


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLE_CHOICES = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    )
MAX_LENGTH_USERNAME = 150
MAX_LENGTH_EMAIL = 254
MAX_LENGTH_ROLE = max(len(role) for role in ROLE_CHOICES)
MAX_LENGTH_CODE = 4
RANGE_CODE = (1000, 9999)


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=MAX_LENGTH_USERNAME, unique=True,
        validators=[validate_username]
    )
    email = models.EmailField(max_length=MAX_LENGTH_EMAIL, unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        max_length=MAX_LENGTH_ROLE, choices=ROLE_CHOICES, default=USER
    )
    confirmation_code = models.CharField(max_length=MAX_LENGTH_CODE)

    class Meta:
        ordering = ('username', )


class BaseModel(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=50, verbose_name='Слаг')

    class Meta:
        abstract = True
        ordering = ('name',)


class Category(BaseModel):
    '''Модель Категории'''

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseModel):
    '''Модель Жанра'''
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    '''Модель Название'''
    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.IntegerField(validators=(correct_year,), verbose_name='Год')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        verbose_name='Жанр'
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    '''Модель Отзывы'''
    text = models.CharField(
        max_length=256,
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        CustomUser, related_name='reviews',
        on_delete=models.CASCADE, verbose_name='Автор'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1, message='Оценка должна быть от 1'),
            MaxValueValidator(10, message='Оценка должна быть до 10')
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата публикации'
    )
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = 'Отзыв произведения'
        verbose_name_plural = 'Отзывы произведений'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]
        ordering = ('pub_date', )


class Comments(models.Model):
    '''Модель комментарии'''
    text = models.CharField(max_length=256, verbose_name='Текст')
    author = models.ForeignKey(
        CustomUser, related_name='comments',
        on_delete=models.CASCADE
    )
    review = models.ForeignKey(
        Review, related_name='comments',
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date', )
