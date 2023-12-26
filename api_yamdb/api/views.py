from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets

from api.models import Category
from .serializer import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    
    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)
