# bookshelf/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book

# View list of books
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

# Add a book
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        published_at = request.POST.get('published_at')

        Book.objects.create(
            title=title,
            author=author,
            description=description,
            published_at=published_at,
            added_by=request.user
        )
        return redirect('book_list')
    return render(request, 'bookshelf/book_form.html')

# Edit a book
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.description = request.POST.get('description')
        book.published_at = request.POST.get('published_at')
        book.save()
        return redirect('book_list')
    return render(request, 'bookshelf/book_form.html', {'book': book})

# Delete a book
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('book_list')
