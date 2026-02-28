import django_filters as filters
from django.contrib.auth import get_user_model
from library.models import (
    Author, Category,
    Book, BorrowRecord
)


User = get_user_model()


class UserFilter(filters.FilterSet):
    user_id = filters.UUIDFilter(field_name='user_id')
    username = filters.CharFilter(
        field_name='username', lookup_expr='icontains'
    )
    email = filters.CharFilter(
        filter_name='email', lookup_expr='icontians'
    )
    role = filters.ChoiceFilter(
        field_name='role',
        choices=User.Role.choices
    )
    created_after = filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte'
    )
    created_before = filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte'
    )


    class Meta:
        model = User
        fields = []


class AuthorFilter(filters.FilterSet):
    author_id = filters.UUIDFilter(field_name='author_id')
    name = filters.CharFilter(field_name='name', lookup_expr='icontians')
    created_after = filters.DateTimeFilter(
        field_name='created_at', lookup_expr='gte'
    )
    created_before = filters.DateTimeFilter(
        field_name='created_at', lookup_expr='lte'
    )

    class Meta:
        model = Author
        fields = []


class CategoryFilter(filters.FilterSet):
    category_id = filters.UUIDFilter(filed_name='category_id')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    created_after = filters.DateTimeFilter(
        field_name='created_at', lookup_expr='gte'
    )
    created_before = filters.DateTimeFilter(
        field_name='created_at', lookup_expr='lte'
    )

    class Meta:
        model = Category
        fields = []


class BookFilter(filters.FilterSet):
    book_id = filters.UUIDFilter(field_name='book_id')
    title = filters.CharFilter(field_name='title', lookup_expr='icontians')
    authors = filters.UUIDFilter(field_name='authors__author_id')
    categories = filters.UUIDFilter(
        field_name='categories__category_id'
    )
    isbn = filters.CharFilter(field_name='isbn', lookup_expr='icontains')
    publication_date = filters.DateTimeFilter(
        field_name='publication_date', lookup_expr='gte'
    )
    created_after = filters.DateTimeFilter(
        field_name='created_at', lookup_expr='gte'
    )
    created_beore = filters.DateTimeFilter(
        field_name='created_at', lookup_expr='lte'
    )

    class Meta:
        model = Book
        fields = []


class BorrowRecordFilter(filters.FilterSet):
    record_id = filters.UUIDFilter(field_name='record_id')
    user_id = filters.UUIDFilter(field_name='user__user_id', lookup_expr='exact')
    user_username = filters.CharFilter(
        field_name='user__username', lookup_expr='icontains'
    )
    book_id = filters.UUIDFilter(
        field_name='book__book_id', lookup_expr='exact'
    )
    book_title = filters.CharFilter(
        field_name='book__title', lookup_expr='icontains'
    )
    due_date = filters.DateTimeFilter(
        field_name='due_date', lookup_expr='gte'
    )
    returned_at = filters.DateTimeFilter(
        field_name='returned_at',
        lookup_expr='gte'
    )

    class Meta:
        model = BorrowRecord
        fields = []
