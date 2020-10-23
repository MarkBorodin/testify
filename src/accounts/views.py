from accounts.forms import AccountCreateForm, AccountPasswordChangeForm, AccountUpdateForm
from accounts.models import User

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView


class AccountCreateView(CreateView):
    model = User
    template_name = 'registration.html'
    form_class = AccountCreateForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, 'you have successfully registered')
        return result


class AccountLoginView(LoginView):
    template_name = 'login.html'

    def get_redirect_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return reverse('core:index')

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, 'you have successfully logged in')
        return result


class AccountLogoutView(LogoutView):
    template_name = 'logout.html'

    def get_next_page(self):
        result = super().get_next_page()
        messages.success(self.request, 'you have successfully logged out')
        return result


class AccountUpdateView(UpdateView):
    model = User
    template_name = 'profile.html'
    form_class = AccountUpdateForm
    success_url = reverse_lazy('core:index')

    def get_object(self, queryset=None):
        return self.request.user


class AccountPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'password-change.html'
    form_class = AccountPasswordChangeForm
    success_url = reverse_lazy('core:index')


class AccountListView(ListView):
    model = User
    template_name = 'users-list.html'
    context_object_name = 'users'


class LeaderboardListView(ListView):
    model = User
    template_name = 'leaderboard.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.filter(rating__gt=0).order_by('-rating')
        context['users'] = users
        return context
