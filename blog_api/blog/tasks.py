from celery import shared_task
import smtplib
from email.mime.text import MIMEText

from django.contrib.auth.models import User
from environs import Env

from .models import Blog, Post

env = Env()
env.read_env()

MY_EMAIL = env.str("MY_EMAIL")
MY_EMAIL_PASSWORD = env.str("MY_EMAIL_PASSWORD")


@shared_task
def send_daily_email():
    """
    A function to send daily email
    :return:
    """
    users = User.objects.all()
    for user in users:
        if user.email and user.email.strip():
            followed_blogs = Blog.objects.filter(follower__in=[user])
            posts = Post.objects.filter(blog__in=followed_blogs).order_by("-create_time")[:5]
            email_content = '\n'.join([str(post) for post in posts])

            msg = MIMEText(email_content)
            msg["From"] = MY_EMAIL
            msg["To"] = user.email
            msg["Subject"] = "New 5 posts"

            try:
                server = smtplib.SMTP(MY_EMAIL, 587)
                server.starttls()
                server.login(MY_EMAIL, MY_EMAIL_PASSWORD)
                server.sendmail(MY_EMAIL, [user.email],
                                msg.as_string())
                server.quit()
                print("Email sent successfully.")
            except Exception as e:
                print(f"Error sending email: {e}")
        else:
            print("User has no email")
