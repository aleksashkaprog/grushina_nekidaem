from django.contrib import admin

from .models import Post, Blog, ViewedPost


class BlogAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(Blog, BlogAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'create_time', 'blog']


admin.site.register(Post, PostAdmin)


class ViewedPostAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']


admin.site.register(ViewedPost, ViewedPostAdmin)
