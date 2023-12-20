from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CategoryViewSet


app_name = 'api'
router_v1 = SimpleRouter()
router_v1.register('categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
