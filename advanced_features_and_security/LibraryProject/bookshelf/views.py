# bookshelf/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.db import transaction
from .models import Book
from .forms import BookForm, BookSearchForm

# LIST / SEARCH — uses validated form input for search
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    form = BookSearchForm(request.GET or None)
    qs = Book.objects.all().order_by("-published_at")
    if form.is_valid():
        q = form.cleaned_data.get("q")
        if q:
            # Using ORM filters avoids SQL injection and is safe
            qs = qs.filter(title__icontains=q)  # parameterized by Django ORM
    # Pagination could be added here
    return render(request, "bookshelf/book_list.html", {"books": qs, "search_form": form})

# CREATE
@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
@require_http_methods(["GET", "POST"])
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            # Use transaction.atomic for safer write operations
            with transaction.atomic():
                book = form.save(commit=False)
                book.added_by = request.user
                book.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "bookshelf/form_example.html", {"form": form, "action": "Create"})

# EDIT
@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
@require_http_methods(["GET", "POST"])
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            with transaction.atomic():
                form.save()
            return redirect("book_list")
    else:
        form = BookForm(instance=book)
    return render(request, "bookshelf/form_example.html", {"form": form, "action": "Edit"})

# DELETE
@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
@require_http_methods(["POST"])
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # Use POST for destructive action and CSRF protection is enforced by CsrfViewMiddleware
    book.delete()
    return redirect("book_list")
