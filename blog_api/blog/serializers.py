from rest_framework import serializers

from .models import Blog, Post, ViewedPost


class BlogSerializer(serializers.ModelSerializer):
    """A serializer for Blog model."""

    def subscribe(self, user):
        """
        A method for subscribing on blog
        :param user:
        :return: instance
        """
        instance = self.instance
        instance.follower.add(user)
        instance.save()
        return instance

    def unsubscribe(self, user):
        """
        A method for subscribing on blog
        :param user:
        :return: instance
        """
        instance = self.instance
        instance.follower.remove(user)
        instance.save()
        return instance

    def get_posts(self, user):
        """
        A method for getting blog's posts
        :param user:
        :return: user_posts
        """
        user_blogs = user.blog.follower.all()
        user_posts = Post.objects.filter(blog__in=user_blogs)
        return user_posts

    class Meta:
        model = Blog
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    """A serializer for Blog model."""
    def add_post_to_viewed(self, user, post):
        """
        A method for adding post to viewed
        :param user:
        :param post:
        :return: answer of success
        """
        try:
            ViewedPost.objects.get(user=user, post=post)
            return {"success": "пост уже был добавлен в прочитанные"}
        except ViewedPost.DoesNotExist:
            ViewedPost.objects.create(user=user, post=post)
            return {"success": "пост успешно добавлен в прочитанные"}

    class Meta:
        model = Post
        fields = "__all__"
