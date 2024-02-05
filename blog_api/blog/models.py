from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Blog(models.Model):
    """
    Models of blog
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='blog', verbose_name='владелец')
    follower = models.ManyToManyField(User, related_name='followers',
                                      verbose_name='подписчики')

    @receiver(post_save, sender=User)
    def create_user_blog(sender, instance, created, **kwargs):
        if created:
            Blog.objects.create(user=instance)


class Post(models.Model):
    """
    Model of post
    """
    title = models.CharField(max_length=20, null=False, blank=False, verbose_name='заголовок')
    text = models.CharField(max_length=140, verbose_name='текст')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='posts', verbose_name='блог')

    def __str__(self):
        return self.title


class ViewedPost(models.Model):
    """
    Model of viewed post
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users', verbose_name='пользователь')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posts', verbose_name='пост')
