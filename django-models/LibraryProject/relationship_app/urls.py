# Python
from django.urls import path, include
from django.contrib import admin

urlpatterns = [path('admin/', admin.site.urls),
    path('books/', list_books, name='list_books'),  # FBV
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # CB
    path('relationship/', include('relationship_app.urls')),
    path('admin/', admin.site.urls),
    ]