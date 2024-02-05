from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Blog
from .serializers import BlogSerializer


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
