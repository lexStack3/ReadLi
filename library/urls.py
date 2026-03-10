from django.urls import path
from .views import (
    HomeView,
    BooksView,
    BookDetailView,
    CategoriesView,
    AuthorsView,
    DashboardView,
    LoginView,
    SignupView
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("books/", BooksView.as_view(), name="books"),
    path("book/<uuid:pk>/", BookDetailView.as_view(), name="book"),
    path("categories/", CategoriesView.as_view(), name="categories"),
    path("authors/", AuthorsView.as_view(), name="authors"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
]