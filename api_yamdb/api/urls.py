from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (SignupView, TokenView, UserList, UserDetail,
                    UserDetailForAdmin, CategoryViewSet,
                    GenreViewSet, TitleViewSet, ReviewViewSet,
                    CommentsViewSet)


app_name = 'api'
router_v1 = SimpleRouter()
router_v1.register('categories', CategoryViewSet, basename='сategories')
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

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('v1/auth/token/', TokenView.as_view(), name='token'),
    path('v1/users/me/', UserDetail.as_view(), name='user_detail'),
    # path(
    #     r'v1/users/(?P<username>[\w.@+-]+)/',
    #     UserDetailForAdmin.as_view(),
    #     name='user'
    # ),
    path('v1/users/', UserList.as_view(), name='users'),
    path(
        'v1/users/<str:username>/',
        UserDetailForAdmin.as_view(), name='user'),
    path('v1/', include(router_v1.urls)),
]
