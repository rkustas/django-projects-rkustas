from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from ..models import Board, Post, Topic
from ..views import PostDeleteView
from django.forms import ModelForm



class PostDeleteViewTestCase(TestCase):
    # Base test to be used in all subsequent tests
    def setUp(self):
        self.board = Board.objects.create(
            name="Django", description="Django board.")
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(
            username=self.username, email="john@doe.com", password=self.password)
        self.topic = Topic.objects.create(
            subject='Hello, world', board=self.board, starter=user)
        self.post = Post.objects.create(
            message="Lorem ipsum dolor sit amet", topic=self.topic, created_by=user)
        self.url = reverse('remove_post', kwargs={
            'pk': self.board.pk,
            'topic_pk': self.topic.pk,
            'post_pk': self.post.pk
        })

class LoginRequiredPostDeleteViewTests(PostDeleteViewTestCase):
    def test_redirection(self):
        # Test if only logged in users can edit posts
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(
            login_url=login_url, url=self.url))


class UnauthorizedPostDeleteViewTests(PostDeleteViewTestCase):
    def setUp(self):
        # Create a new user different from the one that posted
        super().setUp()
        username = 'jane'
        password = '321'
        user = User.objects.create_user(
            username=username, email='jane@doe.com', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        # Topic should only be edited by the owner.  Unauthorized users get a 404
        self.assertEquals(self.response.status_code, 404)


class PostDeleteViewTests(PostDeleteViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.delete(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 302)

    def test_view_class(self):
        view = resolve('/boards/1/topics/1/posts/1/remove/')
        self.assertEquals(view.func.view_class, PostDeleteView)


class SuccessfulPostDeleteViewTests(PostDeleteViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.delete(self.url)

    def test_redirection(self):
        # '''
        # A valid form submission should redirect the user
        # '''
        topic_posts_url = reverse('topic_posts', kwargs={
                                  'pk': self.board.pk, 'topic_pk': self.topic.pk})
        self.assertRedirects(self.response, topic_posts_url)

    def test_post_deleted_response(self):
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 404)

    def test_post_deleted(self):
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
    
