from django.shortcuts import render
from .models import Book

# Function-based view: List all books with their authors
def list_books(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'list_books.html', {'books': books})
from django.views.generic import DetailView
from .models import Library
# Class-based view: Detail view for a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'
