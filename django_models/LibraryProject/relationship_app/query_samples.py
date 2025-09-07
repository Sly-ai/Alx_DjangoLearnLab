from relationship_app.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
author_name = "George Orwell"
books_by_author = Book.objects.filter(author__name=author_name)
for book in books_by_author:
    print(book.title)

# 2. List all books in a specific library
library_name = "Central Library"
library = Library.objects.get(name=library_name)
for book in library.books.all():
    print(book.title)

# 3. Retrieve the librarian for a library
librarian = Librarian.objects.get(library=library)
print(librarian.name)
# 4. Find all authors who have books in a specific library