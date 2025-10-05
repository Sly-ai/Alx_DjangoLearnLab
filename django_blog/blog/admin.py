from django.contrib import admin
from .models import Post, Comment  # assuming Post already registered

# Register your models here.

admin.site.register(Comment)