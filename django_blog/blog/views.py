from django.shortcuts import render

# Home page
def index(request):
    return render(request, 'blog/home.html')

# Blog posts list
def post_list(request):
    return render(request, 'blog/posts_list.html')

# Login page
def login_view(request):
    return render(request, 'blog/login.html')

# Register page
def register_view(request):
    return render(request, 'blog/register.html')
