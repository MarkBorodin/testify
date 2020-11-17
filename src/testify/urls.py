from django.urls import path

from testify.views import QuestionView, TestDetailView, TestListView, TestRunnerView

app_name = 'tests'

urlpatterns = [
    path('', TestListView.as_view(), name='list'),
    path('<int:id>/', TestDetailView.as_view(), name='details'),
    path('<int:id>/start/', TestRunnerView.as_view(), name='start'),
    path('<int:id>/next/', QuestionView.as_view(), name='next'),
]

# handler404 = 'testify.views.error_404'
# handler500 = 'testify.views.error_500'
# handler403 = 'testify.views.error_403'
# handler400 = 'testify.views.error_400'
