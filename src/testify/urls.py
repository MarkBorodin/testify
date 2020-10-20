from django.urls import path

from testify.views import TestListView

app_name = 'testify'

urlpatterns = [
    path('', TestListView.as_view(), name='tests'),
]
