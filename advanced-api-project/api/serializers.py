from .models import Author, Book
from rest_framework import serializers

# Create your serializers here.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

# Nested serializer to include books within author representation
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
    
    def validate_date_of_publication(self, publication_year):
        # Example validation: Ensure publication year is not in the future
        if publication_year > 2025:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return publication_year