from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from library.models import Book, Author, Category, BorrowRecord


class HomeView(ListView):
    model = Book
    template_name = "index.html"
    context_object_name = "books"


class BooksView(ListView):
    model = Book
    template_name = "books.html"
    context_object_name = "books"


class BookDetailView(DetailView):
    model = Book
    template_name = "book.html"
    context_object_name = "book"


class CategoriesView(ListView):
    model = Category
    template_name = "categories.html"
    context_object_name = "categories"


class AuthorsView(ListView):
    model = Author
    template_name = "authors.html"
    context_object_name = "authors"


class DashboardView(LoginRequiredMixin, ListView):
    model = BorrowRecord
    template_name = "dashboard.html"
    context_object_name = "records"
    login_url = "login"


class LoginView(TemplateView):
    template_name = "login.html"


class SignupView(TemplateView):
    template_name = "signup.html"
