from django.urls import path, include
from .views import BookList, BookViewSet, index
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='books')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),
    # Endpoint for obtaining authentication token for API access
    path('api-token/', obtain_auth_token, name='api_token_auth'),
    path('', index, name='index'),  # Home page
]