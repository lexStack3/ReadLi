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
