from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import (
    MAX_LENGTH_EMAIL, MAX_LENGTH_USERNAME, Category, Comment, Genre, Review,
    Title
)
from reviews.validators import validate_username

User = get_user_model()


class ValidateUsernameMixin(serializers.Serializer):
    def validate_username(self, username):
        return validate_username(username)


class SignupSerializer(ValidateUsernameMixin, serializers.Serializer):
    email = serializers.EmailField(
        max_length=MAX_LENGTH_EMAIL, required=True
    )
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME, required=True
    )


class TokenSerializer(ValidateUsernameMixin, serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME, required=True
    )
    confirmation_code = serializers.CharField(
        max_length=settings.MAX_LENGTH_CODE, required=True
    )


class UserSerializerForAdmin(
    ValidateUsernameMixin, serializers.ModelSerializer
):
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
    rating = serializers.IntegerField(read_only=True, default=None)

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
        return TitleReadSerializer(instance).data


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
