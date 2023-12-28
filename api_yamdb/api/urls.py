from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet, CommentsViewSet


app_name = 'api'
router_v1 = SimpleRouter()
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register('reviews', ReviewViewSet)
router_v1.register('comments', CommentsViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]