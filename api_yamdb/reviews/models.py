from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from reviews.validators import correct_year


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


class BaseModel(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=50, verbose_name='Слаг')

    class Meta:
        abstract = True


class Category(BaseModel):
    '''Модель Категории'''

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseModel):
    '''Модель Жанры'''
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
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


# class GenreTitle(models.Model):
#     genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
#     title = models.ForeignKey(Title, on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = 'Жанр и Произвенение'
#         verbose_name_plural = 'Жанры и Произведения'


class Review(models.Model):
    '''Модель Отзывы'''
    text = models.CharField(
        max_length=256,
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        MyUser, related_name='reviews',
        on_delete=models.CASCADE
    )
    score = models.PositiveSmallIntegerField(
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


class Comments(models.Model):
    '''Модель комментарии'''
    text = models.CharField(max_length=256, verbose_name='Текст комментария')
    author = models.ForeignKey(
        MyUser, related_name='comments',
        on_delete=models.CASCADE
    )
    reviews = models.ForeignKey(
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
