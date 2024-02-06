import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()


import random

from django.contrib.auth.models import User
from django.db import transaction
from faker import Faker


fake = Faker()


def create_users(n):
    """Функция для создания пользователей"""
    for _ in range(n):
        username = fake.user_name()
        email = fake.email()
        password = 'password'
        user, created = User.objects.get_or_create(username=username, email=email)
        user.set_password(password)
        user.save()


def create_follossers(n, max_followers_for_blog=10000):
    """Функция для создания пользователей"""
    for _ in range(random.randint(1, max_followers_for_blog)):
        username = fake.user_name()
        email = fake.email()
        password = 'password'
        user, created = User.objects.get_or_create(username=username, email=email)
        user.set_password(password)
        user.save()


@transaction.atomic
def create_followers(users, max_followers_per_user=10000):
    """Функция для добавления подписчиков блогам пользователей"""
    for user in users:
        # Получаем блог пользователя, куда будем добавлять подписчиков
        user_blog = Blog.objects.get(user=user)

        # В качестве подписчиков выбираем случайных пользователей, избегая самого пользователя
        potential_followers = [u for u in users if u != user]

        # Ограничиваем максимальное количество подписчиков для блога
        num_followers = random.randint(1, max_followers_per_user)

        # Добавляем подписчиков
        for _ in range(num_followers):
            follower = random.choice(potential_followers)

            # Добавляем пользователя как подписчика блога, если он уже не подписан
            if not user_blog.follower.filter(id=follower.id).exists():
                user_blog.follower.add(follower)

            # Предотвращаем повторное добавление того же подписчика
            potential_followers.remove(follower)


def create_posts(users, max_posts_per_user=1000):
    """Функция для создания постов в блогах пользователей"""
    for user in users:
        for _ in range(random.randint(1, max_posts_per_user)):
            title = fake.sentence(nb_words=6)[:20]
            text = fake.text(max_nb_chars=140)
            blog = user.blog
            Post.objects.create(title=title, text=text, blog=blog)


def create_views(users, posts, max_views_per_post=10000):
    """Функция для создания просмотров постов"""
    for post in posts:
        viewers = random.sample(users, random.randint(1, max_views_per_post))
        for user in viewers:
            ViewedPost.objects.get_or_create(user=user, post=post)


num_users = 1000000
create_users(num_users)

users = User.objects.all()
create_followers(users)  # Добавлен вызов новой функции
create_posts(users)
posts = Post.objects.all()
create_views(users, posts)

print("Data generation completed!")
