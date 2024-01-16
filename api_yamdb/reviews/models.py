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
MAX_LENGTH_ROLE = max(len(role) for tuple in ROLE_CHOICES for role in tuple)
MAX_LENGTH_CODE = 5
RANGE_CODE = (10000, 99999)


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=MAX_LENGTH_USERNAME, unique=True,
        validators=[validate_username],
        verbose_name='Никнейм'
    )
    email = models.EmailField(
        max_length=MAX_LENGTH_EMAIL, unique=True,
        verbose_name='E-mail'
    )
    bio = models.TextField(blank=True, verbose_name='Биография')
    role = models.CharField(
        max_length=MAX_LENGTH_ROLE, choices=ROLE_CHOICES, default=USER,
        verbose_name='Роль'
    )
    confirmation_code = models.CharField(
        max_length=MAX_LENGTH_CODE, blank=True, null=True,
        editable=False, verbose_name='Код подтверждения'
    )

    class Meta:
        ordering = ('username', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username} ({self.role})'


class BaseModel(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=50, verbose_name='Слаг')

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name} || {self.slug}'


class Category(BaseModel):
    '''Модель Категории'''

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Genre(BaseModel):
    '''Модель Жанра'''
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)


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

    def __str__(self):
        genres = ', '.join(genre.slug for genre in self.genre.all())
        description = self.description if self.description else "N/A"
        return (f'{self.name[:20]} || {self.year} || {self.category.slug[:20]}'
                f' || {genres[:20]} || {description[:20]}')


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
        on_delete=models.DO_NOTHING,
        verbose_name='Произведение'
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

    def __str__(self):
        return (f'{self.text[:20]} || {self.author.username[:20]} || '
                f'{self.title.name[:20]} || {self.score} || '
                f'{self.pub_date: %Y-%m-%d %H:%M:%S}')


class Comments(models.Model):
    '''Модель комментарии'''
    text = models.CharField(max_length=256, verbose_name='Текст')
    author = models.ForeignKey(
        CustomUser, related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review, related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Отзыв произведения'
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date', )

    def __str__(self):
        return (f'{self.text[:20]} || {self.author.username[:20]} || '
                f'{self.review.text[:20]} || '
                f'{self.pub_date: %Y-%m-%d %H:%M:%S}')
