from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet


router = routers.DefaultRouter()

router.register(r'accounts', UserViewSet, basename='accounts')

urlpatterns = [
    path('', include(router.urls)),
]
