from bookshelf.models import Book

# Fetch and update the book's title
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Expected output:
# <Book: Nineteen Eighty-Four by George Orwell>
