import os
import random
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_api.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Blog, Post, ViewedPost

from django.db import transaction
from faker import Faker

fake = Faker()


def create_users(n):
    """A function for creating users test data"""
    for i in range(n):
        username = fake.user_name()
        email = fake.email()
        password = 'password'
        user, created = User.objects.get_or_create(username=username + str(i), email=email)
        blog, created = Blog.objects.get_or_create(user=user)
        user.set_password(password)
        user.save()
        blog.save()


@transaction.atomic
def create_followers(users, max_followers_per_user=500):
    """A function for creating followers test data"""
    for user in users:
        user_blog = Blog.objects.get(user=user)

        num_followers = random.randint(1, max_followers_per_user)
        chosen_followers = set()

        while len(chosen_followers) < num_followers:
            follower = random.choice(users)

            if follower != user and follower not in chosen_followers:
                user_blog.follower.add(follower)
                chosen_followers.add(follower)


def create_posts(users, max_posts_per_user=500):
    """A function for creating posts test data"""
    for user in users:
        for _ in range(random.randint(1, max_posts_per_user)):
            title = fake.sentence(nb_words=6)[:20]
            text = fake.text(max_nb_chars=140)
            Post.objects.create(title=title, text=text, blog=user.blog)


def create_views(users, posts, max_views_per_post=500):
    """A function for creating views of posts test data"""""
    for post in posts:
        viewers = random.sample(list(users), random.randint(1, max_views_per_post))
        for user in viewers:
            ViewedPost.objects.get_or_create(user=user, post=post)


num_users = 1000
create_users(num_users)

create_users(num_users)
print("Пользователи созданы")
users = User.objects.all()
create_followers(users)
print("Подписчики созданы")
create_posts(users)
print("Посты созданы")
posts = Post.objects.all()
create_views(users, posts)
print("Просмотры созданы")

print("Data generation completed!")
