from django import forms
from .models import Post, Profile, Comment, Tag
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from taggit.forms import TagWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']  # Author is set automatically
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Write your post content here...'}),
            'tags': TagWidget(),
        }
    
    # user-facing comma-separated tags field (not a direct model field)
    tags_field = forms.CharField(
        required=False,
        help_text="Add tags separated by commas (e.g. django,python,tutorial)",
        widget=forms.TextInput(attrs={'placeholder': 'django, python, tutorial'})
    )

    def __init__(self, *args, **kwargs):
        # if instance passed, populate tags_field with existing tags
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['tags_field'].initial = ', '.join([t.name for t in self.instance.tags.all()])

    def clean_tags_field(self):
        raw = self.cleaned_data.get('tags_field', '')
        # Normalize: split by comma, strip whitespace, remove empties, unique-lowercase
        names = [n.strip() for n in raw.split(',') if n.strip()]
        normalized = []
        for n in names:
            if n.lower() not in [x.lower() for x in normalized]:
                normalized.append(n)
        return normalized  # list of tag names

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'avatar')

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}),
        max_length=2000,
        label=''
    )

    class Meta:
        model = Comment
        fields = ['content']