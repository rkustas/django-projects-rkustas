from datetime import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.urls.base import reverse_lazy
from django.views.generic import View, CreateView, UpdateView, ListView
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse, resolve

# Class based views login_required decorator import
from django.utils.decorators import method_decorator

# Import models
from .models import Board, Topic, Post

# Import forms
from .forms import NewTopicForm, NewPostForm

# All boards


# def home(request):
#     boards = Board.objects.all()

#     return render(request, 'home.html', {"boards": boards})

# Home rewrite using GCBV
class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'

# View function for topics per board


# def board_topics(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     # Create a field on the fly to access in the template as topic.replies
#     queryset = board.topics.order_by(
#         '-last_updated').annotate(replies=Count('posts') - 1)
#     # function based pagination
#     page = request.GET.get('page', 1)
#     paginator = Paginator(queryset, 20)

#     try:
#         topics = paginator.page(page)
#     except PageNotAnInteger:
#         # Fallback to the first page
#         topics = paginator.page(1)
#     except EmptyPage:
#         # User trys to enter a number that exceeds the range, so we fallback to last page
#         topics = paginator.page(paginator.num_pages)

#     # Topics is now a paginator.Page instance instead of a queryset
#     return render(request, 'topics.html', {"board": board, 'topics': topics})

# Paginatinon using the list view GCBV


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by(
            '-last_updated').annotate(replies=Count('posts')-1)
        return queryset

# New topic added view


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()  # TODO get the currently logged in user
    if request.method == 'POST':
        # Create a form instance
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'), topic=topic, created_by=user)

            # TODO redirect to the created topic once created
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        # if the request is a GET just initialize a blank form
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('topic_posts', kwargs={
                                'pk': pk, 'topic_pk': topic_pk})
            # Building a url with the last page and adding an anchor to the element with id equals to the post ID
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_post_url)
    else:
        form = NewPostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


# def topic_posts(request, pk, topic_pk):
#     topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
#     topic.views += 1
#     topic.save()
#     return render(request, "topic_posts.html", {'topic': topic})

# GCBV for listing posts


class PostsListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        # So the same user that just continues to refesh a page doesn't add to views
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get(
            'pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


def new_post(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = NewPostForm()
    return render(request, 'new_post.html', {'form': form})

# class based view


class NewPostView(View):

    def render(self, request):
        return render(request, 'new_post.html', {'form': self.form})

    def post(self, request):
        form = NewPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
        return self.render(request)

    def get(self, request):
        form = NewPostForm()
        return self.render(request)


# Generic Class Based Views
# class NewPostView(CreateView):
#     model = Post
#     form_class = NewPostForm
#     success_url = reverse_lazy('post_list')
#     template_name = 'new_post.html'

# All requests pass through the dispatch method
@method_decorator(login_required, name="dispatch")
class PostUpdateView(UpdateView):
    model = Post
    # Can define form_class or fields, use fields for simple forms, explicitly define you form for complex forms
    fields = ('message',)
    template_name = "edit_post.html"
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    # Override get_queryset of class to make sure the user that posted can only edit the post
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter the queryset so only the logged in user which is available in the request can edit
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)
