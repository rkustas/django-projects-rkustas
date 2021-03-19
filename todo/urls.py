# Urls for site

# Import path
from django.urls import path
# Import all views
from . import views

urlpatterns = [
    path('', views.index, name='index')
]
