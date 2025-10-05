from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Library
from .forms import BookForm
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

# Create your views here.
# Function-based view: List all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "list_books.html", {"books": books})

# Class-based view: Show details of a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = "library_detail.html"
    context_object_name = "library"

# Register view
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after register
            return redirect("list_books")  # redirect to books page
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

# Login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("list_books")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

# Book list view
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

# Logout view
@login_required
def logout_view(request):
    logout(request)
    return render(request, "logout.html")

# Role checks
def is_admin(user):
    return user.is_authenticated and getattr(user, 'userprofile', None) and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and getattr(user, 'userprofile', None) and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and getattr(user, 'userprofile', None) and user.userprofile.role == 'Member'


@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'admin_view.html')


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'librarian_view.html')


@user_passes_test(is_member)
def member_view(request):
    return render(request, 'member_view.html')

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

# Edit book view
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form})

# Delete book view
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'confirm_delete.html', {'book': book})