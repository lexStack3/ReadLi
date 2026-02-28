import uuid
from django.utils import timezone
from django.db import models, transaction
from django.contrib.auth import get_user_model
from accounts.models import BaseModel


User = get_user_model()


class Author(BaseModel):
    """
    Model representation of an <Author> instance.
    """
    author_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=100)
    biography = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(
                fields=['name'],
                name='author_name_idx'
            )
        ]

    def __str__(self):
        """
        String representation of an <Author> instance.
        """
        return f"{self.name}"


class Category(BaseModel):
    """
    Model representation of a <Category> instance.
    """
    category_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        """
        String representation of a <Category> instance.
        """
        return self.name


class Book(BaseModel):
    """
    Model representation of a <Book> instance.
    """
    book_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    authors = models.ManyToManyField(Author, related_name="books")
    categories = models.ManyToManyField(Category, related_name="books")

    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()

    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)

    class Meta:
        indexes = [
            models.Index(
                fields=['title'],
                name='title_idx'
            ),
        ]

    def __str__(self):
        """
        String representation of a <Book> instance.
        """
        return self.title


class BorrowRecord(BaseModel):
    """
    Model representation of a <BorrowRecord> instance.
    """
    record_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="borrow_records"
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="borrow_records"
    )
    due_date = models.DateField()
    returned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        """
        String representation of a <BorrowRecord> instance.
        """
        return f"{self.user.username} borrowed {self.book.title}"

    @property
    def is_returned(self):
        return self.returned_at is not None

    @property
    def borrowed_at(self):
        return self.created_at

    def return_book(self):
        """
        Returns a book.
        """
        if self.returned_at:
            return False

        with transaction.atomic():
            self.returned_at = timezone.now()
            self.save(update_fields=['returned_at'])

            self.book.available_copies += 1
            self.book.save(update_fields=['available_copies'])

        return True
