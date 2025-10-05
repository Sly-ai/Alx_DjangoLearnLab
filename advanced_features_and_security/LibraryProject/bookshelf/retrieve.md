# Assuming the book you just created has an ID of 1.
# You can find the actual ID from the previous print statement or by querying.
retrieved_book_by_id = Book.objects.get(pk=book.pk)
print(f"Retrieved by ID: {retrieved_book_by_id.title}")