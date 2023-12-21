from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404


from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ['id']


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация Review."""

    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        """Валидация отзывов."""
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                title=title, author=request.user
            ).exists():
                raise ValidationError(
                    'Вы не можете добавить больше'
                    'одного отзыва на произведение'
                )
        return data

    def validate_score(self, value):
        """Валидация рейтинга."""
        if value < 1 or value > 10:
            raise ValidationError(
                f'Недопустимое значение! {value} Доступны значения от 1 до 10.'
            )
        return value

    class Meta:
        """Мета."""

        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация Comment."""

    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        """Мета."""

        model = Comment
        fields = '__all__'
