# Generated by Django 4.2.9 on 2024-02-05 09:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_blog_follower_on"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="blog",
            name="follower_on",
        ),
    ]
