from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from blog.models import Blog, Post

from blog.serializers import BlogSerializer, PostSerializer


class BlogListViewTest(TestCase):
    """Test for Blog list view"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', email='test@example.com', password='testpassword')
        self.url = reverse('blog-list')

    def test_get_blog_list(self):
        """Test for get_method"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerysetEqual(
            response.data,
            Blog.objects.order_by('-id'),
            serializer_class=BlogSerializer
        )


class SingleBlogViewTest(TestCase):
    """Test for single blog view"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('blog-detail', kwargs={'pk': self.user.blog.id})
        self.false_url = reverse('blog-detail', kwargs={'pk': 2})

    def test_get_single_blog_success(self):
        """Test for success get method"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, BlogSerializer(self.user.blog).data)

    def test_get_single_blog_not_found(self):
        """Test that is there no blog, will 404 error"""
        response = self.client.get(self.false_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_blog_subscribe_unsubscribe(self):
        """Test patch method"""
        response = self.client.patch(self.url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostFeedViewTest(TestCase):
    """Test for Post feed view"""
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', email='test@example.com', password='testpassword')
        self.blog = Blog.objects.create(id=1, title='Test Blog')
        for i in range(10):
            self.post = Post.objects.create(title=str(i))
            self.blog.posts.add(self.post)
        self.blog.followers.add(self.user)
        self.url = reverse('feed')

    def test_get_post_feed(self):
        """Test for get_method"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerysetEqual(
            response.data,
            Post.objects.order_by('-create_time'),
            serializer_class=BlogSerializer
        )


class SinglePostViewTest(TestCase):
    """Test for single Post view"""
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', email='test@example.com', password='testpassword')
        self.post = Post.objects.create(title="title", text="text")
        self.client.force_authenticate(user=self.user)
        self.url = reverse('single-post', kwargs={'pk': self.post.id})

    def test_get_single_post(self):
        """Test get method"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, PostSerializer(self.post).data)

    def test_add_post_to_viewed(self):
        """Test adding post to viewed success"""
        data = {}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('viewed', response.data)
        self.assertTrue(response.data['viewed'])

    def test_add_post_to_viewed_post_not_exists(self):
        """Test adding post to viewed if post isn't exist"""
        url = reverse('single-post-view', kwargs={'pk': 99999})
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserCreateViewTest(TestCase):
    """Test for user create view"""

    def test_create_user(self):
        """Test post method"""
        response = self.client.post(self.url, data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, self.user_data['username'])
