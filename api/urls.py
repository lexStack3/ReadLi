from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, AuthorViewSet


router = routers.DefaultRouter()

router.register(r'accounts', UserViewSet, basename='accounts')
router.register(r'authors', AuthorViewSet, basename='authors')

urlpatterns = [
    path('', include(router.urls)),
]
