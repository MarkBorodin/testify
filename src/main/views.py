from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ClientForm, CommentForm, LessonsForm, PostForm
from .models import Client, Comment, Lessons, Post


class SuperUserCheckMixin(UserPassesTestMixin, View):
    """mixin for checking superuser"""
    def test_func(self):
        return self.request.user.is_superuser


class PostCreateView(SuperUserCheckMixin, CreateView):
    """create posts and show them"""
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("main:posts")
    template_name = "make_post.html"

    def get_context_data(self, **kwargs):
        kwargs["posts"] = Post.objects.all()
        return super().get_context_data(**kwargs)


class PostsListView(LoginRequiredMixin, ListView):
    """show all posts and comment to them"""
    model = Post
    form_class = CommentForm
    success_url = reverse_lazy("main:posts")
    template_name = "posts_list.html"

    def get_context_data(self, **kwargs):
        kwargs["posts"] = Post.objects.all()
        kwargs["comments"] = Comment.objects.all()
        return super().get_context_data(**kwargs)


class PostsUpdateView(SuperUserCheckMixin, UpdateView):
    """post editing"""
    model = Post
    template_name = "update_post.html"
    context_object_name = "post"
    form_class = PostForm
    success_url = reverse_lazy("main:posts")


class PostDeleteView(SuperUserCheckMixin, DeleteView):
    """delete post"""
    model = Post
    template_name = "delete_post.html"
    success_url = reverse_lazy("main:make_post")


class CommentCreateView(LoginRequiredMixin, CreateView):
    """create a comment on the selected post"""
    model = Comment
    form_class = CommentForm
    success_url = reverse_lazy("main:posts")
    template_name = "detail_post.html"

    def get_context_data(self, **kwargs):
        kwargs["post"] = Post.objects.get(id=self.kwargs["pk"])
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        post = Post.objects.get(id=self.kwargs["pk"])
        user = self.request.user
        form = form.save(commit=False)
        form.post = post
        form.user = user
        form.save()
        context = {
            'posts': Post.objects.all(),
            'comments': Comment.objects.all()
        }
        return render(self.request, 'posts_list.html', context)


class ClientCreateView(SuperUserCheckMixin, CreateView, ListView):
    """create a new client"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("main:clients")
    template_name = "clients.html"
    paginate_by = 20
    context_object_name = "clients"


class ClientUpdateView(SuperUserCheckMixin, UpdateView):
    """update client data"""
    model = Client
    template_name = "edit_client.html"
    context_object_name = "clients"
    form_class = ClientForm
    success_url = reverse_lazy("main:clients")


class ClientDeleteView(SuperUserCheckMixin, DeleteView):
    """delete client"""
    model = Client
    template_name = "delete_client.html"
    success_url = reverse_lazy("main:clients")


class LessonsCreateView(SuperUserCheckMixin, CreateView):
    """create a lesson"""
    model = Lessons
    form_class = LessonsForm
    success_url = reverse_lazy("main:lessons")
    template_name = "create_lesson.html"


class LessonsListView(SuperUserCheckMixin, ListView):
    """show lessons by filters"""
    model = Lessons
    success_url = reverse_lazy("main:lessons")
    template_name = "lessons.html"
    paginate_by = 20
    context_object_name = "this_month_lessons"

    def get_context_data(self, **kwargs):
        kwargs['today_lessons'] = Lessons.objects.filter(date__date=datetime.today())
        kwargs['tomorrow_lessons'] = Lessons.objects.filter(date__date=datetime.today() + timedelta(days=1))
        kwargs["sum_today_lessons"] = len(kwargs['today_lessons'])

        days = [
            (1, 'sunday'), (2, 'monday'), (3, 'tuesday'), (4, 'wednesday'),
            (5, 'thursday'), (6, 'friday'), (7, 'saturday')
        ]
        querysets = []
        for day, day_of_week in days:
            one_day_lessons = Lessons.objects.filter(date__week_day=day, date__gte=(datetime.now() - timedelta(days=1)),
                                                     date__lte=(datetime.now() + timedelta(days=6))).order_by("date")

            item = {
                'index': day,
                'lessons': one_day_lessons,
                'day_of_week': day_of_week,
            }
            querysets.append(item)

        kwargs['querysets'] = sorted(querysets, key=lambda k: k['index'])
        return super().get_context_data(**kwargs)


class LessonsPerMonthListView(SuperUserCheckMixin, ListView):
    """show lessons per month (for the current month)"""
    model = Lessons
    success_url = reverse_lazy("main:lessons")
    template_name = "lessons_per_month.html"
    paginate_by = 20
    context_object_name = "this_month_lessons"

    def get_queryset(self):
        lessons = super().get_queryset()
        today = datetime.today()
        datem = datetime(today.year, today.month, 1)
        this_month_lessons = lessons.filter(date__gte=datem).order_by("date")
        return this_month_lessons

    def get_context_data(self, **kwargs):
        kwargs["sum_this_month_lessons"] = len(self.get_queryset())
        return super().get_context_data(**kwargs)


class LessonsUpdateView(SuperUserCheckMixin, UpdateView):
    """edit lesson"""
    model = Lessons
    template_name = "edit_lesson.html"
    form_class = LessonsForm
    success_url = reverse_lazy("main:lessons")


class LessonsDeleteView(SuperUserCheckMixin, DeleteView):
    """delete lesson"""
    model = Lessons
    template_name = "delete_lesson.html"
    success_url = reverse_lazy("main:lessons")


def about(request):
    return render(request, "about.html")


def courses(request):
    return render(request, "courses.html")
