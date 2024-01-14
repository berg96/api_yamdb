import re

from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from .validators import UsernameValidator
from reviews.models import (Category, Comments, Genre, Review, Title,
                            MAX_LENGTH_CODE)

User = get_user_model()

MAX_LENGTH_EMAIL = 254
MAX_LENGTH_USERNAME = 150


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=MAX_LENGTH_EMAIL, required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME, required=True,
        validators=[
            UsernameValidator(), UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]

    def validate(self, data):
        username = data['username']
        email = data['email']
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

    # def validate_username(self, value):
    #     _ = get_object_or_404(User, username=value)
    #     return value


class UserSerializerForAdmin(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME, required=True,
        validators=[
            UsernameValidator(), UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserSerializer(UserSerializerForAdmin):
    class Meta(UserSerializerForAdmin.Meta):
        extra_kwargs = {
            'role': {'read_only': True}
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
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
