from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import (Category, Comments, Genre, Review, Title,
                            MAX_LENGTH_CODE, MAX_LENGTH_EMAIL,
                            MAX_LENGTH_USERNAME)
from reviews.validators import validate_username


User = get_user_model()


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=MAX_LENGTH_EMAIL, required=True,
    )
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME, required=True,
        validators=[validate_username]
    )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            if User.objects.get(email=email).username != username:
                raise serializers.ValidationError(
                    'Введенный email уже используется другим пользователем'
                )
        if User.objects.filter(username=username).exists():
            if User.objects.get(username=username).email != email:
                raise serializers.ValidationError(
                    'Введенный email не соответствует '
                    'зарегистрированному username'
                )
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME, required=True
    )
    confirmation_code = serializers.CharField(
        max_length=MAX_LENGTH_CODE, required=True
    )


class UserSerializer(serializers.ModelSerializer):
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
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title

    def get_rating(self, obj):
        if obj.reviews.count() == 0:
            return None
        rev = Review.objects.filter(
            title=obj
        ).aggregate(rating=Avg('score'))
        return rev['rating']


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
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if Review.objects.filter(
            author=self.context['request'].user,
            title_id=self.context['view'].kwargs.get('title_id')
        ).exists() and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Нельзя оставить два отзыва на одно произведение.')
        return data


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments
        read_only_fields = ('title', 'author')
