from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Profile, Comment, Tag
from .forms import PostForm, CustomUserCreationForm, UserUpdateForm, ProfileForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

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
    form_class = PostForm
    paginate_by = 5  # 5 posts per page

# Show a single post
class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author').all()
        return context

# Create a new post
class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        # Handle tags
        tag_names = form.cleaned_data.get('tags_field', [])
        self._update_post_tags(self.object, tag_names)
        return response
    
    def _update_post_tags(self, post, tag_names):
        post.tags.clear()
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name__iexact=name, defaults={'name': name})
            post.tags.add(tag)

# Update a post (author only)
class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
   
    def form_valid(self, form):
        response = super().form_valid(form)
        # Handle tags
        tag_names = form.cleaned_data.get('tags_field', [])
        self._update_post_tags(self.object, tag_names)
        return response
    
    def _update_post_tags(self, post, tag_names):
        post.tags.clear()
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name__iexact=name, defaults={'name': name})
            post.tags.add(tag)
    
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

# Create comment for a given post
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'  # used if someone navigates directly

    def dispatch(self, request, *args, **kwargs):
        # ensure the post exists and keep it for later use
        self.post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})

# Update comment (author-only)
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def get_queryset(self):
        # optionally restrict to comments under the post to ensure path consistency
        return Comment.objects.filter(post__pk=self.kwargs.get('post_pk'))

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.get_object().post.pk})

# Delete comment (author-only)
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_queryset(self):
        return Comment.objects.filter(post__pk=self.kwargs.get('post_pk'))

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.get_object().post.pk})

# List posts by tag
class TaggedPostListView(ListView):
    model = Post
    template_name = 'blog/posts_list.html'  # reuse list template (filtering posts)
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        # case-insensitive match
        return Post.objects.filter(tags__name__iexact=tag_name).order_by('-published_date')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tag_name'] = self.kwargs.get('tag_name')
        return ctx

# Search results view
class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        if not q:
            return Post.objects.none()
        # search title, content, and tag name (case-insensitive)
        return Post.objects.filter(
            Q(title__icontains=q) | Q(content__icontains=q) | Q(tags__name__icontains=q)
        ).distinct().order_by('-published_date')