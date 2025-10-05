from django.contrib import admin
from .models import Book

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Customizes the display and management of the Book model in the Django admin.
    """
    # The list_display option controls which fields are displayed in the change list page.
    # It takes a tuple of field names as strings.
    # The order of the field names determines the column order in the table.
    list_display = ('title', 'author', 'publication_year')

    # The list_filter option provides a sidebar for filtering results.
    # It takes a tuple of field names. You can use model fields or custom filters.
    list_filter = ('author', 'publication_year')

    # The search_fields option adds a search box to the admin page.
    # Django will perform a search on the specified fields.
    # Use a leading underscore to perform a lookup on a related field, e.g., 'author__name'.
    search_fields = ('title', 'author')

    # The list_per_page option sets the number of items to display per page.
    # This is an optional customization.
    list_per_page = 25