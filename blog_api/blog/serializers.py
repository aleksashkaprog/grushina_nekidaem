from rest_framework import serializers

from .models import Blog


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

    class Meta:
        model = Blog
        fields = ['id', 'user', 'follower']
