from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.test import APITestCase


# 📖 List all books (read-only allowed for unauthenticated users)
# List all books with filtering, searching, and ordering
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    # Add filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtering: exact matches
    filterset_fields = ['title', 'author', 'publication_year']

    # Searching: partial matches
    search_fields = ['title', 'author']

    # Ordering: sort results
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering


# 📖 Retrieve a single book (read-only allowed for unauthenticated users)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # anyone can view


# ➕ Create a new book (only authenticated users)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # must be logged in

    def perform_create(self, serializer):
        # Attach the user who created the book
        serializer.save(created_by=self.request.user)


# ✏️ Update a book (only authenticated users)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # must be logged in

    def update(self, request, *args, **kwargs):
        # Example: block invalid titles
        if "forbidden" in request.data.get("title", "").lower():
            return Response(
                {"error": "This title is not allowed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)


# ❌ Delete a book (only authenticated users)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # must be logged in

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