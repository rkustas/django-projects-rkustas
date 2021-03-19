from django.http import response
from django.test import TestCase, testcases
from django.urls import resolve, reverse
from ..views import signup
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Forms
from ..forms import SignUpForm


# Create your tests here.


class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def text_contains_form(self):
        form = self.resonse.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        # Five inputs required
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'john',
            'email': 'john@doe.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.boards_url = reverse('home')

    def test_redirection(self):
        # Valid form submission redirects user to home page
        self.assertRedirects(self.response, self.boards_url)

    def test_user_create(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        # Create a response to an arbitrary page and the result should now have a 'user' to its context after successful signup
        response = self.client.get(self.boards_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})  # Submit empty data

    def test_signup_status_code(self):
        # Invalid form submission returns to signup page
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
