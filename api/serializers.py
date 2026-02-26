from rest_framework import serializers
from django.contrib.auth import get_user_model

from library.models import (
    Author, Category,
    Book, BorrowRecord
)


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    A <User> model serializer.
    """

    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'email',
            'first_name', 'last_name', 'role',
            'created_at', 'updated_at'
        ]
        read_only_fields = (
            'user_id', 'created_at', 'updated_at',
            'role'
        )


class AuthorBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['book_id', 'title']


class AuthorSerializer(serializers.ModelSerializer):
    """
    An <Author> model serializer.
    """
    books = AuthorBookSerializer(read_only=True, many=True)

    class Meta:
        model = Author
        fields = [
            'author_id', 'name', 'biography', 'date_of_birth',
            'books', 'created_at', 'updated_at'
        ]


class CategoryBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['book_id', 'title']


class CategorySerializer(serializers.ModelSerializer):
    """
    A <Category> model serializer.
    """
    books = CategoryBooksSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'category_id', 'name', 'description', 'books',
            'created_at', 'updated_at'
        ]


class BookCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'name']


class BookAuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['author_id', 'name']


class BookSerializer(serializers.ModelSerializer):
    """
    A <Book> model serializer.
    """
    authors = BookAuthorsSerializer(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        source='authors',
        queryset=Author.objects.all()
    )
    categories = BookCategoriesSerializer(read_only=True, many=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        source='categories',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Book
        fields = [
            'book_id', 'title', 'description', 'isbn',
            'publication_date', 'total_copies', 'available_copies',
            'author_ids', 'authors', 'categories', 'category_ids',
            'created_at', 'updated_at'
        ]
