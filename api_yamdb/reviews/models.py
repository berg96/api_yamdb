from django.contrib.auth import get_user_model
from django.db import models

from api.validators import correct_year

User = get_user_model()


class BaseModel(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=50, verbose_name='Слаг')

    class Meta:
        abstract = True


# ---------------------------------------------------------------------------------------
# CATEGORIES
# категории CATEGORIES,
# name - required - string <= 256 characters
# slug - required - string <= 50 characters ^[-a-zA-Z0-9_]+$

class Category(BaseModel):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

# ---------------------------------------------------------------------------------------
# жанров GENRES;
# реализует импорта данных из csv файлов.
# name - required - string <= 256 characters
# slug - required - string <= 50 characters ^[-a-zA-Z0-9_]+$

class Genre(BaseModel):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

# ---------------------------------------------------------------------------------------
# TITLES
# произведения TITLES,
# category - string - фильтрует по полю slug категории 
# genre - string - фильтрует по полю slug жанра
# name - string -фильтрует по названию произведения <= 256 characters
# year - integer - фильтрует по году

class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.IntegerField(validators=(correct_year,), verbose_name='Год')

# Нужно определить связанность
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True,
        verbose_name='Категория'
    )
# Нужно определить связанность
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


# Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению.
# Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.