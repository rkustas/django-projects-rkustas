from django.http import response
from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

# Import views
from ..views import board_topics, new_topic, BoardListView

# Import Models
from ..models import Board, Topic, Post

# Import forms
from ..forms import NewTopicForm


class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(
            name="Django", description="Django board.")
        url = reverse('home')
        self.response = self.client.get(url)

    def test_boards_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_boards_url_resolves_home_view(self):
        view = resolve('/boards/')
        self.assertEquals(view.func.view_class, BoardListView)

    def test_board_view_contains_link_to_topics_page(self):
        board_topics_url = reverse(
            'board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(
            self.response, 'href="{0}"'.format(board_topics_url))
