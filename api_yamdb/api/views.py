from rest_framework import viewsets

from .serializers import CategorySerializer
from .permissions import AdminOrReadOnly
from api_yamdb.reviews.models import Category, Genre, Title


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = AdminOrReadOnly
