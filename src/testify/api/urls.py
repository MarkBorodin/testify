from django.urls import path

from testify.api.views import TestListCreateView, TestUpdateDeleteView

app_name = 'testify'

urlpatterns = [
    path('tests/', TestListCreateView.as_view(), name='list'),
    path('tests/<int:pk>/', TestUpdateDeleteView.as_view(), name='details'),
]
