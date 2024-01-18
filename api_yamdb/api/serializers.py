from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import (
    MAX_LENGTH_CODE, MAX_LENGTH_EMAIL,MAX_LENGTH_USERNAME, Category, Comment,
    Genre, Review, Title
)
from reviews.validators import validate_username

User = get_user_model()


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=MAX_LENGTH_EMAIL, required=True
    )
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME, required=True,
        validators=[validate_username]
    )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME, required=True,
        validators=[validate_username]
    )
    confirmation_code = serializers.CharField(
        max_length=MAX_LENGTH_CODE, required=True
    )


class UserSerializerForAdmin(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME, required=True,
        validators=[
            validate_username, UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserSerializer(UserSerializerForAdmin):
    class Meta(UserSerializerForAdmin.Meta):
        read_only_fields = ('role', )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.FloatField(read_only=True, default=None)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Title

    def to_representation(self, instance):
        representation = TitleReadSerializer(instance)
        return representation.data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'POST' and Review.objects.filter(
            author=self.context['request'].user,
            title_id=self.context['view'].kwargs.get('title_id')
        ).exists():
            raise serializers.ValidationError(
                'Нельзя оставить два отзыва на одно произведение.')
        return data


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
