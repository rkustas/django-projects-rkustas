from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.urls.base import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required


# Class based views login_required decorator import
from django.utils.decorators import method_decorator

# Forms
from .forms import SignUpForm

# Create your views here.

# Signup request


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@method_decorator(login_required, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user
