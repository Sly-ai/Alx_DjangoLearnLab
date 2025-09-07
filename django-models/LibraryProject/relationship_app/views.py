from django.shortcuts import render
from django.views.generic import DetailView

# Create your views here.
from .models import Book

# Function-based view to list all books
def list_books(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'list_books.html', {'books': books})

from .models import Library

# Class-based view to show details for a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'
