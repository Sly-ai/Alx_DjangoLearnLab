from relationship_app.models import Author, Book, Library, Librarian

# Example: Query all books by a specific author
author_name = "George Orwell"  # replace with any existing author in your database
author = Author.objects.get(name=author_name)  # <- REQUIRED LINE
books_by_author = Book.objects.filter(author=author)  # <- REQUIRED LINE
for book in books_by_author:
    print(book.title)

# Example: List all books in a library
library = Library.objects.get(name="library_name")
books_in_library = library.books.all()
for book in books_in_library:
    print(book.title)

# Example: Retrieve the librarian for a library
librarian = Librarian.objects.get(library=library)
print(librarian.name)
