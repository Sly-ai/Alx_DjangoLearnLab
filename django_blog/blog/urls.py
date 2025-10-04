from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),             # Home page
    path('posts/', views.post_list, name='posts'),  # Blog posts
    path('login/', views.login_view, name='login'), # Login page
    path('register/', views.register_view, name='register'), # Register page
]
