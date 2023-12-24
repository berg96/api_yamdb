from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import SignupView, TokenView


app_name = 'api'
router_v1 = SimpleRouter()

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('v1/auth/token/', TokenView.as_view(), name='token'),
]
