from django.urls import include, path
from rest_framework.routers import SimpleRouter


app_name = 'api'
router_v1 = SimpleRouter()

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]