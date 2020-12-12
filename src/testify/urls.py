from django.urls import path

from testify.views import QuestionView, ResultListView, TestDetailView, TestListView, TestRunnerView

app_name = 'tests'

urlpatterns = [
    path('', TestListView.as_view(), name='list'),
    path('results', ResultListView.as_view(), name='results'),
    path('<int:id>/', TestDetailView.as_view(), name='details'),
    path('<int:id>/start/', TestRunnerView.as_view(), name='start'),
    path('<int:id>/next/', QuestionView.as_view(), name='next'),
]
