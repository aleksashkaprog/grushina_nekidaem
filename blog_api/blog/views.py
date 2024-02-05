from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Blog, Post
from .serializers import BlogSerializer, PostSerializer, UserSerializer


class BlogListView(ListAPIView):
    """
    A view for list of blogs
    """
    queryset = Blog.objects.order_by('-id')
    serializer_class = BlogSerializer

    def get(self, request, *args, **kwargs):
        """
        A method for getting blogs
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return self.list(request, *args, **kwargs)


class SingleBlogView(APIView):
    """
    A view for one blog
    """

    def get(self, request, pk):
        """
        A method for get blog's data
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
        A method for subscribing and unsubscribing on blog
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


class PostFeedPagination(PageNumberPagination):
    """
    A class representing pagination for Post Feed.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 500


class PostFeedView(APIView):
    """
    A view for post feed
    """
    pagination_class = PostFeedPagination

    def get(self, request, pk):
        """
        A method for getting feed of posts
        :param request:
        :param pk:
        :return: response
        """
        user = User.objects.get(id=pk)
        followed_blogs = Blog.objects.filter(follower__in=[user])
        posts = Post.objects.filter(blog__in=followed_blogs).order_by("-create_time")
        serializer = PostSerializer(posts, many=True)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(posts, request, view=self)

        if page is not None:
            return paginator.get_paginated_response(serializer.data)

        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)


class SinglePostView(APIView):
    """
    A view for one post
    """

    def get(self, request, pk):
        """
        A method for get blog's data
        :param request:
        :param pk:
        :return: Response
        """
        post = Post.objects.get(id=pk)
        post_serializer = PostSerializer(post)
        post_data = post_serializer.data

        return Response(post_data)

    def post(self, request, pk):
        """
        A method for adding post to viewed
        :param request:
        :param pk:
        :return: Response
        """
        post = Post.objects.get(id=pk)
        post_serializer = PostSerializer(post)
        user = request.user
        post_data = post_serializer.add_post_to_viewed(user, post)

        return Response(post_data)


class UserCreateView(CreateAPIView):
    """
    A view for creating user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
