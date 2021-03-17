from django.contrib import admin
from .models import Post, Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'content', 'date_posted']
    list_filter = ['post', 'date_posted']
    search_fields = ['name', 'post', 'content']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_posted', 'author']
    list_filter = ['date_posted', 'author']
    search_fields = ['title', 'content', 'author']

