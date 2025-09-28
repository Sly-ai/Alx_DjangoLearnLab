from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend



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

