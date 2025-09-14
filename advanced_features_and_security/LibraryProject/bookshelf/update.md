# Retrieve the book again if you closed the shell or are starting fresh
book_to_update = Book.objects.get(title="The Hitchhiker's Guide to the Galaxy")

# Update the title
book_to_update.title = "The Restaurant at the End of the Universe"
book_to_update.save() # This is crucial to persist the changes

print(f"Book updated. New title: {book_to_update.title}")