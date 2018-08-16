from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View


from .auth_forms import SignUpForm

from django.contrib.auth.views import LoginView


class LoginView(LoginView):
    template_name = 'login.html'
    authentication_form = AuthenticationForm

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return redirect('exercises')


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('signup_success')
    template_name = 'signup.html'


class SignUpSuccess(generic.TemplateView):
    template_name = 'account/signup_success.html'


class AccountView(LoginRequiredMixin, View):
    context_object_name = 'experiments'
    template_name = 'account/account.html'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs.get('username'))
        if user == request.user:
            experiments = []
            return render(request, self.template_name, {self.context_object_name: experiments})

        return redirect('home')


def index(request):
    form = SignUpForm()
    return render(request, 'home.html', {'form': form})