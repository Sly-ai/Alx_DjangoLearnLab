from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book        # link it to the Book model
        fields = '__all__'  # include *all* fields (title, author, year)
