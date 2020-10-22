from django.urls import path

from testify.views import QuestionView, TestDetailView, TestListView, TestRunnerView

app_name = 'tests'

urlpatterns = [
    path('', TestListView.as_view(), name='list'),
    path('<int:id>/', TestDetailView.as_view(), name='details'),
    path('<int:id>/start/', TestRunnerView.as_view(), name='start'),
    path('<int:id>/question/<int:order_number>', QuestionView.as_view(), name='question'),
]
