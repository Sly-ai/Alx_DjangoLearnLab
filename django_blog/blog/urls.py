from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='home'),             # Home page
    path('posts/', views.post_list, name='posts'),  # Blog posts
    path('login/', views.login_view, name='login'), # Login page
    path('register/', views.register_view, name='register'), # Register page
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    path('post/new/', views.PostCreate.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdate.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDelete.as_view(), name='post-delete'),
    # Authentication (login/logout use Django's built-ins)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),

    # Registration & profile (custom)
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # Commenting
    path('post/<int:post_pk>/comments/new/', views.CommentCreateView.as_view(), name='comment-create'),
    path('post/<int:post_pk>/comments/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('post/<int:post_pk>/comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),


]
