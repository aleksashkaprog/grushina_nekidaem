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
    """A function for creating users test data"""""
    for _ in range(n):
        username = fake.user_name()
        email = fake.email()
        password = 'password'
        user, created = User.objects.get_or_create(username=username, email=email)
        user.set_password(password)
        user.save()


@transaction.atomic
def create_followers(users, max_followers_per_user=500):
    """A function for creating followers test data"""""
    for user in users:
        user_blog = Blog.objects.get(user=user)

        potential_followers = [u for u in users if u != user]
        num_followers = random.randint(1, max_followers_per_user)

        for _ in range(num_followers):
            follower = random.choice(potential_followers)

            if not user_blog.follower.filter(id=follower.id).exists():
                user_blog.follower.add(follower)

            potential_followers.remove(follower)


def create_posts(users, max_posts_per_user=500):
    """A function for creating posts test data"""""
    for user in users:
        for _ in range(random.randint(1, max_posts_per_user)):
            title = fake.sentence(nb_words=6)[:20]
            text = fake.text(max_nb_chars=140)
            blog = user.blog
            Post.objects.create(title=title, text=text, blog=blog)


def create_views(users, posts, max_views_per_post=500):
    """A function for creating views of posts test data"""""
    for post in posts:
        viewers = random.sample(list(users), random.randint(1, max_views_per_post))
        for user in viewers:
            ViewedPost.objects.get_or_create(user=user, post=post)


num_users = 10000
create_users(num_users)

create_users(num_users)
users = User.objects.all()
create_followers(users)
create_posts(users)
posts = Post.objects.all()
create_views(users, posts)

print("Data generation completed!")
