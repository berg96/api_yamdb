

from rest_framework import serializers

from api.models import Category, Genre, Title




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