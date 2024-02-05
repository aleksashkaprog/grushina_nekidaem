from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Blog, Post
from .serializers import BlogSerializer, PostSerializer


class BlogListView(ListAPIView):
    queryset = Blog.objects.order_by('-id')
    serializer_class = BlogSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SingleBlogView(APIView):
    def get(self, request, pk):
        """
        Method for get blog's data
        :param request:
        :param pk:
        :return: Response
        """
        blog = Blog.objects.get(id=pk)
        blog_serializer = BlogSerializer(blog)
        blog_data = blog_serializer.data

        return Response(blog_data)

    def patch(self, request, pk):
        """
        Method for subscribing and unsubscribing on blog
        :param request:
        :param pk:
        :return: Response
        """
        blog = Blog.objects.get(id=pk)
        user = request.user
        blog_serializer = BlogSerializer(blog, data=request.data, partial=True)

        if user in blog.follower.all():
            blog_serializer.unsubscribe(user)
            return Response({'success': f"Пользователь {user} успешно отписался от блога"})
        else:
            blog_serializer.subscribe(user)
            return Response({'success': f"Пользователь {user} успешно подписался на блог"})


class ArticlePagePagination(PageNumberPagination):
    """A class representing pagination for Article pages."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 500


class PostFeedView(APIView):
    pagination_class = ArticlePagePagination

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        followed_blogs = Blog.objects.filter(follower__in=[user])
        posts = Post.objects.filter(blog__in=followed_blogs).order_by('create_time')
        serializer = PostSerializer(posts, many=True)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(posts, request, view=self)

        if page is not None:
            return paginator.get_paginated_response(serializer.data)

        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)
