from django.conf import settings
from django.core.mail import send_mail

from accounts.forms import AccountCreateForm, AccountPasswordChangeForm, AccountUpdateForm, ContactUs
from accounts.models import User

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, FormView


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
    queryset = User.objects.filter(rating__gt=0).order_by('-rating')


class ContactView(LoginRequiredMixin, FormView):
    template_name = 'contact_us.html'
    extra_context = {'title': 'Send us message!'}
    success_url = reverse_lazy('core:index')
    form_class = ContactUs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            send_mail(
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
                from_email=request.user.email,
                recipient_list=[settings.EMAIL_HOST_RECIPIENT],
                fail_silently=False,
            )
            messages.success(self.request, 'you have successfully sent message')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
