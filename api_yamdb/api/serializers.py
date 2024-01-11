import re

from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from django.db.models import Avg
from rest_framework.validators import UniqueValidator

from reviews.models import (
    Category, Genre, Title, Review, Comments)

User = get_user_model()


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" в качестве username'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=4)


class UserSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(
    #     max_length=150,
    #     validators=[UniqueValidator(queryset=User.objects.all())]
    # )
    # email = serializers.EmailField(
    #     max_length=254,
    #     validators=[UniqueValidator(queryset=User.objects.all())]
    # )
    role = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    # def validate(self, data):
    #     email = data.get('email')
    #     username = data.get('username')
    #     if User.objects.filter(email=email).exists():
    #         user = User.objects.get(email=email)
    #         if user.username != username:
    #             raise serializers.ValidationError(
    #                 {'detail': 'Пользователь с таким email уже существует.'},
    #                 status.HTTP_400_BAD_REQUEST
    #             )
    #     return data

    def validate_username(self, value):
        if not re.fullmatch(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(status.HTTP_400_BAD_REQUEST)
        return value

    # def validate_email(self, value):
    #     if User.objects.filter(email=value).exists():
    #         raise serializers.ValidationError(
    #             {'detail': 'Пользователь с таким email уже существует.'},
    #             status.HTTP_400_BAD_REQUEST
    #         )
    #     return value


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
    rating = serializers.SerializerMethodField()

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
