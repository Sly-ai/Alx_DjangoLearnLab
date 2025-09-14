# Retrieve the book you want to delete
book_to_delete = Book.objects.get(title="The Restaurant at the End of the Universe")

# Delete the book
book_to_delete.delete()

print(f"Book '{book_to_delete.title}' deleted successfully.")

# You can verify deletion by trying to retrieve it again, which should raise a DoesNotExist error
try:
    Book.objects.get(title="The Restaurant at the End of the Universe")
except Book.DoesNotExist:
    print("Verification: Book no longer exists in the database.")