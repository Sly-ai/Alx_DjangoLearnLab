from django.urls import path
from . import views

urlpatterns = [
    path("api/my_app", views.BookListCreateAPIView.as_view(), name="book_list_create"),
    path("", views.home, name="home"),
]