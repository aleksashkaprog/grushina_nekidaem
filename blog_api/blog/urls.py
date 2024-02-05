from django.urls import path

from .views import BlogListView, SingleBlogView

urlpatterns = [
    path("blogs/all", BlogListView.as_view(), name='blog-list'),
    path("blog/<int:pk>", SingleBlogView.as_view(), name='single-blog'),
]