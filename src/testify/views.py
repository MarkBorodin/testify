from django.shortcuts import render # noqa
from django.views.generic import ListView

from testify.models import Test


class TestListView(ListView):
    model = Test
    template_name = 'tests-list.html'
    context_object_name = 'tests'
