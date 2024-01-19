from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_username, validate_year

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLE_CHOICES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)
MAX_LENGTH_USERNAME = 150
MAX_LENGTH_EMAIL = 254
MAX_LENGTH_CODE = 128
MAX_LENGTH_SLUG = 50
MAX_LENGTH_NAME = 256
MAX_LENGTH_NAME_TITLE = 256
MAX_LENGTH_TEXT = 256
MIN_SCORE = 1
MAX_SCORE = 10


class CustomUser(AbstractUser):
    '''Модель Пользователя'''
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
        max_length=max(len(role) for role, _ in ROLE_CHOICES),
        choices=ROLE_CHOICES, default=USER,
        verbose_name='Роль'
    )

    class Meta:
        ordering = ('username', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username} ({self.role})'

    def is_admin(self):
        return self.role == ADMIN or self.is_staff

    def is_moderator(self):
        return self.role == MODERATOR


class BaseSlugModel(models.Model):
    '''Базовая модель для Категории и Жанра'''
    name = models.CharField(
        max_length=MAX_LENGTH_NAME, verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG, unique=True, verbose_name='Слаг'
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} || {self.slug}'


class Category(BaseSlugModel):
    '''Модель Категории'''

    class Meta(BaseSlugModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseSlugModel):
    '''Модель Жанра'''
    class Meta(BaseSlugModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    '''Модель Произведения'''
    name = models.CharField(
        max_length=MAX_LENGTH_NAME_TITLE, verbose_name='Название'
    )
    year = models.IntegerField(validators=(validate_year,), verbose_name='Год')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="titles",
        blank=True, null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre, related_name="titles", verbose_name='Жанр'
    )

    description = models.TextField(
        blank=True, default='', verbose_name='Описание'
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        genres = ', '.join(genre.slug for genre in self.genre.all())
        return (f'{self.name[:20]} || {self.year} || {self.category.slug[:20]}'
                f' || {genres[:20]} || {self.description[:20]}')


class BaseTextAuthorModel(models.Model):
    '''Базовая модель для Отзыва и Комментария'''
    text = models.CharField(max_length=MAX_LENGTH_TEXT, verbose_name='Текст')
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        abstract = True
        ordering = ('pub_date', )
        default_related_name = '%(class)ss'

    def __str__(self):
        return (f'{self.text[:20]} || {self.author.username[:20]} || '
                f'{self.pub_date:%Y-%m-%d %H:%M:%S}')


class Review(BaseTextAuthorModel):
    '''Модель Отзыва'''
    score = models.IntegerField(
        validators=[
            MinValueValidator(
                MIN_SCORE, message=f'Оценка должна быть от {MIN_SCORE}'
            ),
            MaxValueValidator(
                MAX_SCORE, message=f'Оценка должна быть до {MAX_SCORE}'
            )
        ],
        verbose_name='Оценка'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Произведение'
    )

    class Meta(BaseTextAuthorModel.Meta):
        verbose_name = 'Отзыв произведения'
        verbose_name_plural = 'Отзывы произведений'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return super().__str__() + f'|| {self.title.name[:20]} || {self.score}'


class Comment(BaseTextAuthorModel):
    '''Модель комментария'''
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='Отзыв произведения'
    )

    class Meta(BaseTextAuthorModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return super().__str__() + f' || {self.review.text[:20]}'
