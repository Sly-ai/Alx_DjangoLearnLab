book = Book.objects.create(title="The Hitchhiker's Guide to the Galaxy", author="Douglas Adams", published_year=1979)
print(f"Book created: {book.title} by {book.author}")