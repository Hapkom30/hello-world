from django.contrib import admin
from .models import Category, Post, Comment, Subscription, PostCategory

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Subscription)
admin.site.register(Comment)
