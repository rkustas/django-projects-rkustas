"""djangoapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.conf.urls import url
from todo.views import index
from boards.views import new_topic, reply_topic, new_post, NewPostView, PostUpdateView, BoardListView, TopicListView, PostsListView, PostDeleteView, TopicDeleteView
from accounts.views import signup, UserUpdateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name="Todo"),
    url(r'^boards/$', BoardListView.as_view(), name="home"),
    url(r'^boards/(?P<pk>\d+)/$', TopicListView.as_view(), name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/new/$', new_topic, name='new_topic'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    #     template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'),
        name='password_reset_complete'),
    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$',
        PostsListView.as_view(), name='topic_posts'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/remove/$', TopicDeleteView.as_view(), name='remove_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$',
        reply_topic, name='reply_topic'),
    url(r'^new_post/$', new_post, name='new_post'),
    # Class based view
    url(r'^new_post/$', NewPostView.as_view(), name='new_post'),
    # # GCBY
    # url(r'^new_post/$', NewPostView.as_view(), name='new_post'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
        PostUpdateView.as_view(), name='edit_post'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/remove/$',
        PostDeleteView.as_view(), name='remove_post'),
    url(r'^settings/account/$', UserUpdateView.as_view(), name='my_account'),




]
