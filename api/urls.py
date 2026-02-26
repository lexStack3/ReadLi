from django.urls import path, include
from rest_framework import routers

from .views import (
    UserViewSet, AuthorViewSet,
    CategoryViewSet, BookViewSet
)


router = routers.DefaultRouter()

router.register(r'accounts', UserViewSet, basename='accounts')
router.register(r'authors', AuthorViewSet, basename='authors')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
]
