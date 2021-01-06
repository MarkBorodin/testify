from accounts.forms import AccountCreateForm, AccountPasswordChangeForm, AccountUpdateForm, ContactUs, TrialLesson
from accounts.models import User
from accounts.tasks import trial_lesson_email

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView, ListView, UpdateView

from main.views import SuperUserCheckMixin


class AccountCreateView(CreateView):
    """Create Account"""
    model = User
    template_name = 'registration.html'
    form_class = AccountCreateForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, 'you have successfully registered')
        return result


class AccountLoginView(LoginView):
    """account login"""
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
    """Account Logout"""
    template_name = 'logout.html'

    def get_next_page(self):
        result = super().get_next_page()
        messages.success(self.request, 'you have successfully logged out')
        return result


class AccountUpdateView(UpdateView):
    """Account Update"""
    model = User
    template_name = 'profile.html'
    form_class = AccountUpdateForm
    success_url = reverse_lazy('core:index')

    def get_object(self, queryset=None):
        return self.request.user


class AccountPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """change account password"""
    template_name = 'password-change.html'
    form_class = AccountPasswordChangeForm
    success_url = reverse_lazy('core:index')


class AccountListView(SuperUserCheckMixin, ListView):
    """list of users"""
    model = User
    template_name = 'users-list.html'
    context_object_name = 'users'


class LeaderboardListView(SuperUserCheckMixin, ListView):
    """user rating based on test results"""
    model = User
    template_name = 'leaderboard.html'
    context_object_name = 'users'
    queryset = User.objects.filter(rating__gt=0).order_by('-rating')


class ContactView(LoginRequiredMixin, FormView):
    """show the feedback form and send a letter"""
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


class TrialLessonView(LoginRequiredMixin, FormView):
    """when registering for a trial lesson, sends a letter by mail"""
    template_name = 'trial_lesson.html'
    success_url = reverse_lazy('tests:list')
    form_class = TrialLesson

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            trial_lesson_email.delay(
                subject=form.cleaned_data['name'],
                message=str([
                    form.cleaned_data['name'],
                    form.cleaned_data['phone_number'],
                    form.cleaned_data['level'],
                    form.cleaned_data['email'],
                ]),
                from_email=request.user.email,
                recipient_list=[settings.EMAIL_HOST_RECIPIENT],
                fail_silently=False,
            )
            messages.success(self.request, 'Спасибо! Мы свяжемся с Вами по поводу пробного занятия :)'
                                           ' А пока, можете попробовать попроходить тесты ;)')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
