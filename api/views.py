from django.contrib.auth import get_user_model
from rest_framework import viewsets, status

from library.models import (
    Author, Category,
    Book
)
from .serializers import (
    UserSerializer,
    AuthorSerializer,
    CategorySerializer,
    BookSerializer
)


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related('books')
    serializer_class = CategorySerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.prefetch_related('categories')
    serializer_class = BookSerializer
