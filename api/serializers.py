from rest_framework import serializers
from django.contrib.auth import get_user_model

from library.models import (
    Author, Category,
    Book, BorrowRecord
)


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """
    A <User> model serializer for creating a new user.
    """
    password = serializers.CharField(
        write_only=True,
        style={'input_type': "password"}
    )
    password2 = serializers.CharField(
        write_only=True,
        style={'input_type': "password"}
    )

    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'email',
            'first_name', 'last_name', 'role',
            'password', 'password2',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'user_id', 'created_at', 'updated_at',
            'role'
        ]

    def validate(self, attr):
        """
        Validates user password.
        """
        password = attr.get('password')

        if password:
            if attr['password'] != attr['password2']:
                raise serializers.ValidationError(
                    {'password': "Password does not match"}
                )
        return attr

    def create(self, validated_data):
        """
        Creates a new <User> instance.
        """
        password = validated_data.pop('password')
        validated_data.pop('password2')

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Updates a <User> profile.
        """
        password = validated_data.pop('password')
        password1 = validated_data.pop('password2')

        for k, v in validated_data.items():
            setattr(instance, k, v)

        if password:
            if password != password1:
                raise serializers.ValidationError(
                    {'password': "Password does not match"}
                )
            instance.set_password(password)

        instance.save()
        return instance


class UserCreateAdminSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        read_only_fields = ['user_id', 'created_at', 'updated_at']


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


class BorrowBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'book_id', 'title'
        ]

class UserBorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'full_name', 'email', 'role']


class BorrowRecordSerializer(serializers.ModelSerializer):
    """
    A <BorrowRecord> model serializer.
    """
    user = UserBorrowSerializer(read_only=True)
    book_borrowed = BorrowBookSerializer(read_only=True, source='book')
    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
    )

    class Meta:
        model = BorrowRecord
        fields = [
            'record_id', 'book', 'user', 'due_date',
            'book_borrowed', 'is_returned', 'borrowed_at',
            'returned_at', 'updated_at'
        ]
        read_only_fields = ['returned_at']

    def validate(self, attr):
        book = attr['book']

        if book.available_copies == 0:
            raise serializers.ValidationError(
                {"available_copies": "Not enough books left for borrowing."}
            )

        return attr

    def create(self, validated_data):
        request = self.context.get('request')
        book = validated_data.get('book')

        record = BorrowRecord.objects.create(
            book=book,
            user=request.user,
            due_date=validated_data.get('due_date', None)
        )
        book.available_copies -= 1
        book.save(update_fields=['available_copies'])
        return record


class AdminBorrowSerializer(serializers.ModelSerializer):
    """
    A <BorrowRecord> model serializer for admin users.
    """
    borrower = UserBorrowSerializer(read_only=True, source='user')
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )
    book_borrowed = BorrowBookSerializer(read_only=True, source='book')
    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        write_only=True
    )

    class Meta:
        model = BorrowRecord
        fields = [
            'record_id', 'borrower', 'user', 'book_borrowed',
            'book', 'due_date', 'returned_at', 'is_returned',
            'borrowed_at', 'updated_at'
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        book = validated_data.get('book')

        record = BorrowRecord.objects.create(
            book=book,
            user=request.user,
            due_date=validated_data.get('due_date', None)
        )
        record.book.available_copies -= 1
        record.book.save(update_fileds=['available_copies'])
        return record
