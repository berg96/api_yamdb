

from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comments




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
