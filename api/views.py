from django.contrib.auth import get_user_model
from rest_framework import viewsets, status

from library.models import Author
from .serializers import (
    UserSerializer,
    AuthorSerializer,
)


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
