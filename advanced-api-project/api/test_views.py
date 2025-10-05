from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username="testuser", password="pass1234")

        # Create some sample books
        self.book1 = Book.objects.create(
            title="The Hobbit", author="J.R.R. Tolkien", publication_year=1937
        )
        self.book2 = Book.objects.create(
            title="Harry Potter", author="J.K. Rowling", publication_year=1997
        )

        # Authenticated client
        self.client.login(username="testuser", password="pass1234")

    # -------------------------------
    # CRUD Tests
    # -------------------------------

    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        url = reverse("book-detail", args=[self.book1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "The Hobbit")

    def test_create_book_authenticated(self):
        url = reverse("book-create")
        data = {"title": "1984", "author": "George Orwell", "publication_year": 1949}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        self.client.logout()
        url = reverse("book-create")
        data = {"title": "1984", "author": "George Orwell", "publication_year": 1949}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book(self):
        url = reverse("book-update", args=[self.book1.id])
        data = {"title": "The Hobbit: Revised", "author": "J.R.R. Tolkien", "publication_year": 1937}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "The Hobbit: Revised")

    def test_delete_book(self):
        url = reverse("book-delete", args=[self.book2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # -------------------------------
    # Filtering, Searching, Ordering
    # -------------------------------

    def test_filter_books_by_author(self):
        url = reverse("book-list") + "?author=J.K. Rowling"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["author"], "J.K. Rowling")

    def test_search_books(self):
        url = reverse("book-list") + "?search=Hobbit"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "The Hobbit")

    def test_order_books_by_publication_year_desc(self):
        url = reverse("book-list") + "?ordering=-publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # First result should be the latest year
        self.assertEqual(response.data[0]["publication_year"], 1997)