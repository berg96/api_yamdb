from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    CategoryViewSet, CommentsViewSet, GenreViewSet, ReviewViewSet,
    TitleViewSet, UserViewSet, give_token, signup
)

app_name = 'api'
router_v1 = SimpleRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

auth_patterns = [
    path('signup/', signup, name='signup'),
    path('token/', give_token, name='give_token')
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_patterns))
]
