import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from library.models import (
    Author, Category,
    Book, BorrowRecord
)


User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with sample library data"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Seeding database..."))

        # Create User
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@readli.edu",
                password="adminpass"
            )

        if not User.objects.filter(username="member").exists():
            User.objects.create_user(
                username="member",
                email="member@readli.edu",
                password="memberpass"
            )


        # Create Authors
        authors = [
            Author.objects.get_or_create(name="Chinua Achebe")[0],
            Author.objects.get_or_create(name="J.K Rowling")[0],
            Author.objects.get_or_create(name="George Orwell")[0]
        ]

        # Create Categories
        categories = [
            Category.objects.get_or_create(name="Fiction")[0],
            Category.objects.get_or_create(name="Fantasy")[0],
            Category.objects.get_or_create(name="Drama")[0]
        ]

        # Create Books
        book1, _ = Book.objects.get_or_create(
            title="Things Fall Apart",
            isbn="1234567890123",
            publication_date="1958-01-01",
            total_copies=5,
            available_copies=5
        )
        book1.authors.set([authors[0]])
        book1.categories.set([categories[0], categories[2]])

        book2, _ = Book.objects.get_or_create(
            title="Harry Potter and the Philosopher's Stone",
            isbn="1234567890124",
            publication_date="1997-06-26",
            total_copies=10,
            available_copies=10
        )
        book2.authors.set([authors[1]])
        book2.categories.set([categories[0], categories[1]])

        book3, _ = Book.objects.get_or_create(
            title="1984",
            isbn="1234567890125",
            publication_date="1949-06-08",
            total_copies=7,
            available_copies=7
        )
        book3.authors.set([authors[1]])
        book3.categories.set([categories[0]])

        # Create Borrow Record
        member = User.objects.get(username="member")

        if not BorrowRecord.objects.filter(user=member, book=book1).exists():
            BorrowRecord.objects.create(
                user=member,
                book=book1,
                due_date=timezone.now().date() + timedelta(days=14)
            )
            book1.available_copies -= 1
            book1.save()

        self.stdout.write(self.style.SUCCESS("Database seeded successfully"))
