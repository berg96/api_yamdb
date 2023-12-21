"""ФАЙЛ МОДЕЛИ."""
from django.db import models

from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(default=2023)
    description = models.TextField(null=True, blank=True)
    genre = models.ManyToManyField(Genre, related_name='titles')
    category = models.ForeignKey(
        Category, on_delete=models.SET_DEFAULT, default=None,
        related_name='titles'
    )

    class Meta:
        ordering = ('name',)


class CommentReview(models.Model):
    """Абстрактная модель для Review и Comment."""

    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Мета."""

        abstract = True


class Review(CommentReview):
    """Модель отзыва на произведения."""

    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Возможны значения от 1 до 10'),
            MaxValueValidator(10, 'Возможны значения от 1 до 10')
        ]
    )

    class Meta:
        """Мета."""

        ordering = ('pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review'
            ),
        )


class Comment(CommentReview):
    """Модель коменты к отзывам."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    class Meta:
        """Мета."""

        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
