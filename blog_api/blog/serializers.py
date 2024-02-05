from rest_framework import serializers

from .models import Blog, Post


class BlogSerializer(serializers.ModelSerializer):
    """Serializer for Blog model."""

    def subscribe(self, user):
        """
        Method for subscribing on blog
        :param user:
        :return: instance
        """
        instance = self.instance
        instance.follower.add(user)
        instance.save()
        return instance

    def unsubscribe(self, user):
        """
        Method for subscribing on blog
        :param user:
        :return: instance
        """
        instance = self.instance
        instance.follower.remove(user)
        instance.save()
        return instance

    def get_posts(self, user):
        user_blogs = user.blog.follower.all()
        user_posts = Post.objects.filter(blog__in=user_blogs)
        return user_posts

    class Meta:
        model = Blog
        fields = ["id", "user", "follower"]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'create_time', 'blog']
