from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from .forms import PostForm, CustomUserCreationForm, UserUpdateForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy

# Create your views here.
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

# List all posts
class PostList(ListView):
    model = Post
    template_name = 'blog/posts_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

# Show a single post
class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

# Create a new post
class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Update a post (author only)
class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Delete a post (author only)
class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/posts/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created. You can now log in.")
            return redirect('login')  # name of auth login url below
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    # GET: show profile/edit form; POST: save updates
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'blog/profile.html', context)


    