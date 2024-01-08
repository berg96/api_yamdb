from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import(
    Category, Genre, Title, Review, Comments)

User = get_user_model()

class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=4)


class UserSerializer(serializers.ModelSerializer):
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


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'year', 'category', 'genre')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('text', 'author', 'score', 'pub_date')
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('text', 'author', 'pub_date')
        model = Comments