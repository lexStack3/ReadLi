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

        # ----------------------
        # Create Users
        # ----------------------

        users = []

        admin, _ = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@readli.edu",
                "role": User.Role.LIBRARIAN
            }
        )
        admin.set_password("adminpass")
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()
        users.append(admin)

        for i in range(1, 16):
            user, _ = User.objects.get_or_create(
                username=f"member{i}",
                defaults={
                    "email": f"member{i}@readli.edu"
                }
            )
            user.set_password("memberpass")
            user.save()
            users.append(user)

        # ----------------------
        # Create Authors
        # ----------------------

        author_names = [
            "Chinua Achebe", "Wole Soyinka", "Chimamanda Ngozi Adichie",
            "George Orwell", "J.K Rowling", "Stephen King",
            "James Baldwin", "Toni Morrison", "Ngugi wa Thiong'o",
            "Leo Tolstoy", "Fyodor Dostoevsky", "Mark Twain",
            "Jane Austen", "Charles Dickens", "Ernest Hemingway"
        ]

        authors = []

        for name in author_names:
            author, _ = Author.objects.get_or_create(name=name)
            authors.append(author)

        # ----------------------
        # Create Categories
        # ----------------------

        category_names = [
            "Fiction", "Fantasy", "Drama", "Science Fiction",
            "Romance", "Thriller", "Mystery", "Biography",
            "History", "Philosophy", "Technology", "Education",
            "Politics", "Horror", "Adventure"
        ]

        categories = []

        for name in category_names:
            category, _ = Category.objects.get_or_create(name=name)
            categories.append(category)

        # ----------------------
        # Create Books
        # ----------------------

        book_titles = [
            "Things Fall Apart",
            "Half of a Yellow Sun",
            "Purple Hibiscus",
            "1984",
            "Animal Farm",
            "Harry Potter and the Philosopher's Stone",
            "Harry Potter and the Chamber of Secrets",
            "The Shining",
            "It",
            "The Adventures of Tom Sawyer",
            "Pride and Prejudice",
            "War and Peace",
            "Crime and Punishment",
            "Great Expectations",
            "The Old Man and the Sea"
        ]

        books = []

        for i, title in enumerate(book_titles):

            isbn = f"97800000000{i+1}"

            book, _ = Book.objects.get_or_create(
                title=title,
                defaults={
                    "isbn": isbn,
                    "publication_date": "2000-01-01",
                    "total_copies": random.randint(5, 10),
                    "available_copies": random.randint(5, 10),
                }
            )

            # assign authors
            book.authors.set(random.sample(authors, random.randint(1, 2)))

            # assign categories
            book.categories.set(random.sample(categories, random.randint(1, 3)))

            books.append(book)

        # ----------------------
        # Create Borrow Records
        # ----------------------

        borrow_records_created = 0

        while borrow_records_created < 15:
            user = random.choice(users[1:])  # avoid admin
            book = random.choice(books)

            if book.available_copies <= 0:
                continue

            record, created = BorrowRecord.objects.get_or_create(
                user=user,
                book=book,
                defaults={
                    "due_date": timezone.now().date() + timedelta(days=14)
                }
            )

            if created:
                book.available_copies -= 1
                book.save()
                borrow_records_created += 1

        self.stdout.write(self.style.SUCCESS("Database seeded successfully"))
