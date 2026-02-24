import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class User(AbstractUser, BaseModel):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    class Role(models.TextChoices):
        LIBRARIAN = "LIBRARIAN", "Librarian"
        PATRON = "PATRON", "Patron"

    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.PATRON
    )
    email = models.CharField(
        max_length=128, blank=False, unique=True
    )

    class Meta:
        indexes = [
            models.Index(
                fields=['email'],
                name='email_idx'
            )
        ]


    def __str__(self):
        """
        String representation of a <User> model.
        """
        return f"{self.full_name} - {self.role}"

    @property
    def full_name(self):
        """
        Returns a user's username or concatenated first and last names.
        """
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
