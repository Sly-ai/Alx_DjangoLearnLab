from django.shortcuts import render, HttpResponse
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

# Create your views here.
class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

def home(request):
    return HttpResponse("Welcome to Django!")