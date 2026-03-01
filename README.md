# 📚 ReadLi - Library Management System API

ReadLi is a role-based Library Management REST API built with **Django**
and **Django REST Framework**.

It allows librarians to manage books, authors, and categories, while
patrons can securely borrow and return books with proper inventory
tracking.

------------------------------------------------------------------------

## 🚀 Features

-   🔐 Custom User Model (UUID primary key)
-   👥 Role-Based Access Control (Librarian / Patron)
-   📖 Book Management (CRUD)
-   ✍️ Author Management (CRUD)
-   🏷️ Category Management (CRUD)
-   📦 Borrowing System with Inventory Tracking
-   🔄 Atomic Book Return System
-   ⚡ Optimized Querysets using `select_related` and `prefetch_related`
-   🧾 UUID-based resources for production-level safety
-   🛡️ Custom Permission Classes

------------------------------------------------------------------------

## 🏗️ Tech Stack

-   Python 3.12
-   Django
-   Django REST Framework
-   MySQL
-   Django Simple JWT

------------------------------------------------------------------------

## 👤 User Roles

### 📌 Librarian

-   Create, update, and delete:
    -   Authors
    -   Categories
    -   Books
-   View all borrow records
-   Return books
-   Manage patron borrow records

### 📌 Patron

-   View books, authors, categories
-   Borrow books (if copies available)
-   View only their own borrow records

------------------------------------------------------------------------

## 📚 API Endpoints

### 🔐 Users

  Method   Endpoint       Description
  -------- -------------- -----------------------------------
  POST     /users/        Register user
  GET      /users/        List users (Admin/Librarian only)
  GET      /users/{id}/   Retrieve user
  PATCH    /users/{id}/   Update user
  DELETE   /users/{id}/   Delete user

------------------------------------------------------------------------

### ✍️ Authors

  Method   Endpoint         Access
  -------- ---------------- -----------------
  GET      /authors/        Authenticated
  POST     /authors/        Librarian/Admin
  GET      /authors/{id}/   Authenticated
  PATCH    /authors/{id}/   Librarian/Admin
  DELETE   /authors/{id}/   Librarian/Admin

------------------------------------------------------------------------

### 🏷️ Categories

  Method   Endpoint            Access
  -------- ------------------- -----------------
  GET      /categories/        Authenticated
  POST     /categories/        Librarian/Admin
  PATCH    /categories/{id}/   Librarian/Admin
  DELETE   /categories/{id}/   Librarian/Admin

------------------------------------------------------------------------

### 📖 Books

  Method   Endpoint       Access
  -------- -------------- -----------------
  GET      /books/        Authenticated
  POST     /books/        Librarian/Admin
  PATCH    /books/{id}/   Librarian/Admin
  DELETE   /books/{id}/   Librarian/Admin

------------------------------------------------------------------------

### 📦 Borrow Records

  Method   Endpoint               Description
  -------- ---------------------- ------------------------------------
  GET      /borrow/               Patron sees own records
  POST     /borrow/               Borrow a book
  POST     /borrow/{id}/return/   Return book (Librarian/Admin only)

------------------------------------------------------------------------

## 🔁 Borrowing Logic

### 📥 When Borrowing

-   User must be authenticated
-   Book must have available_copies \> 0
-   available_copies decreases by 1
-   Borrow record is created atomically (transaction safe)

### 📤 When Returning

-   Only Librarian/Admin can return
-   returned_at timestamp is set
-   available_copies increases by 1
-   Wrapped in transaction to ensure database consistency

------------------------------------------------------------------------

## 🧠 Architecture Highlights

-   Business logic centralized in models
-   Atomic transactions for inventory safety
-   Role-based permission enforcement
-   Optimized database queries
-   Clean serializer separation (Admin vs Patron)
-   UUID-based object identification

------------------------------------------------------------------------

## 🛠️ Installation

``` bash
git clone https://github.com/lexStack3/ReadLi.git
cd readli
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

------------------------------------------------------------------------

## 🎥 Project Demo Video

[ReadLi - Library Management System](https://youtu.be/tpLu02g4QHE)

------------------------------------------------------------------------

## 👨‍💻 Author

Alexander Edim\
Backend Engineer \| ALX Backend Pro

------------------------------------------------------------------------

## 📌 Project Status

✔ Core functionality complete\
✔ Role-based security implemented\
✔ Inventory tracking implemented\
🔄 Ongoing improvements
