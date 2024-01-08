from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (SignupView, TokenView, UserList, UserDetail,
                    UserDetailForAdmin, CategoryViewSet,
                    GenreViewSet, TitleViewSet, ReviewViewSet,
                    CommentsViewSet)


app_name = 'api'
router_v1 = SimpleRouter()
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register('reviews', ReviewViewSet)
router_v1.register('comments', CommentsViewSet)

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
    path('v1/users/<str:username>/', UserDetailForAdmin.as_view(), name='user'),
    path('v1/', include(router_v1.urls)),
]
