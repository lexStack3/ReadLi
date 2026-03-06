from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny, IsAdminUser,
    IsAuthenticated
)

from library.models import (
    Author, Category,
    Book, BorrowRecord
)
from .serializers import (
    UserCreateSerializer,
    UserCreateAdminSerializer,
    AuthorSerializer,
    CategorySerializer,
    BookSerializer,
    BorrowRecordSerializer,
    AdminBorrowSerializer
)
from .permissions import IsOwner, IsLibrarian, IsNotAuthenticated
from .filters import (
    UserFilter,
    AuthorFilter,
    CategoryFilter,
    BookFilter,
    BorrowRecordFilter
)


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    A <User> model viewset.
    """
    permission_classes = [IsAuthenticated]
    filter_class = UserFilter
    search_fields = ['username', 'email', 'role']

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return User.objects.none()

        if user.is_staff or user.role == User.Role.LIBRARIAN:
            return User.objects.all()

        return User.objects.filter(user_id=user.user_id)

    def get_permissions(self):
        if self.action == 'create':
            return [(IsAdminUser | IsLibrarian | IsNotAuthenticated)()]

        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [(IsOwner | IsLibrarian | IsAdminUser)()]

        return super().get_permissions()

    def get_serializer_class(self):
        user = self.request.user

        if user.is_authenticated:
            if user.is_staff or user.role == User.Role.LIBRARIAN:
                return UserCreateAdminSerializer

        return UserCreateSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """
    An <Author> model viewset.
    """
    queryset = Author.objects.prefetch_related('books')
    serializer_class = AuthorSerializer
    filter_class = AuthorFilter
    search_fields = ['name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [(IsAdminUser | IsLibrarian)()]

        return super().get_permissions()



class CategoryViewSet(viewsets.ModelViewSet):
    """
    A <Category> model viewset.
    """
    queryset = Category.objects.prefetch_related('books')
    serializer_class = CategorySerializer
    filter_class = CategoryFilter
    search_fields = ['name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [(IsAdminUser | IsLibrarian)()]

        return super().get_permissions()


class BookViewSet(viewsets.ModelViewSet):
    """
    A <Book> model viewset.
    """
    serializer_class = BookSerializer
    filter_class = BookFilter
    search_fields = [
        'title', 'isbn', 'authors__name', 'categories__name',
        'available_copies'
    ]

    def get_queryset(self):
        queryset = Book.objects.prefetch_related("categories", "authors")

        # In case of /authors/{author_id}/books route
        author_id = self.kwargs.get('author_pk', None)
        if author_id:
            queryset = queryset.filter(authors__author_id=author_id)

        # In case of /categories/{category_pk}/books route
        category_id = self.kwargs.get('category_pk', None)
        if category_id:
            queryset = queryset.filter(categories__category_id=category_id)

        return queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [(IsAdminUser | IsLibrarian)()]

        return super().get_permissions()


class BorrowViewSet(viewsets.ModelViewSet):
    """
    A <BorrowRecord> model viewset.
    """
    queryset = BorrowRecord.objects.select_related('user', 'book')
    filter_class = BorrowRecordFilter
    search_fields = [
        'user__username', 'user__email', 'book__title',
        'created_at'
    ]

    def get_queryset(self):
        """
        Returns queryset approprately.
        """
        user = self.request.user

        if not user.is_authenticated:
            return BorrowRecord.objects.none()

        if user.role == User.Role.PATRON:
            return BorrowRecord.objects.select_related('user', 'book').filter(user=user)

        return BorrowRecord.objects.select_related('user', 'book')

    def get_permissions(self):
        """
        Grants permission approprately.
        """
        if self.action == 'create':
            return [IsAuthenticated()]

        if self.action in [
            'return', 'update', 'partial_update', 'destroy'
        ]:
            return [(IsAdminUser | IsLibrarian)()]

        return super().get_permissions()

    def get_serializer_class(self):
        """
        Returns approprate serializer base on user.
        """
        user = self.request.user

        if not user.is_authenticated:
            return BorrowRecordSerializer

        if user.is_staff or user.role == User.Role.LIBRARIAN:
            return AdminBorrowSerializer

        return BorrowRecordSerializer


    @action(
        detail=True,
        methods=['GET'],
        url_path='return',
        permission_classes=[IsAdminUser | IsLibrarian]
    )
    def return_book(self, request, pk):
        """
        Returns a book back to the library.
        """
        record = self.get_object()

        if record.return_book():
            return Response(
                {"detail": "Book returned successfully"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"detail": "Book alreadly returned."},
            status=status.HTTP_400_BAD_REQUEST
        )
