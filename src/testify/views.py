from accounts.models import User

from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from testify.forms import AnswerFormSet
from testify.models import Question, Test, TestResult


class TestListView(ListView):
    model = Test
    template_name = 'list.html'
    context_object_name = 'tests'


class TestDetailView(DetailView):
    model = Test
    template_name = 'details.html'
    context_object_name = 'test'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        test_id = self.kwargs['id']
        all_results = TestResult.objects.filter(test=test_id)
        context['all_results'] = all_results
        context['best_result'] = TestResult.best_result(test_id)
        context['last_run'] = TestResult.last_run(test_id)
        return context


class TestRunnerView(View):

    def get(self, request, id):  # noqa
        TestResult.objects.filter(
            user=request.user,
            state=TestResult.STATE.NEW,
            test=Test.objects.get(id=id),
        ).delete()

        TestResult.objects.create(
            user=request.user,
            state=TestResult.STATE.NEW,
            test=Test.objects.get(id=id),
            num_correct_answers=0,
            num_incorrect_answers=0,
        )

        return redirect(reverse('tests:question', args=(id, 1)))


class QuestionView(View):

    def get(self, request, id, order_number):  # noqa
        question = Question.objects.get(test_id=id, order_number=order_number)
        answers = question.answers.all()
        form_set = AnswerFormSet(queryset=answers)

        return render(
            request=request,
            template_name='question.html',
            context={
                'question': question,
                'form_set': form_set,
            }
        )

    def post(self, request, id, order_number):  # noqa
        question = Question.objects.get(test__id=id, order_number=order_number)
        answers = question.answers.all()
        form_set = AnswerFormSet(data=request.POST)

        possible_choices = len(form_set.forms)
        selected_choices = [
            'is_selected' in form.changed_data
            for form in form_set.forms
        ]

        correct_choices = sum(
            answer.is_correct == choice
            for answer, choice in zip(answers, selected_choices)
        )

        point = int(correct_choices == possible_choices)

        test_result = TestResult.objects.get(
            user=request.user,
            test=question.test,
            state=TestResult.STATE.NEW
        )

        test_result.num_correct_answers += point
        test_result.num_incorrect_answers += (1 - point)
        test_result.save()

        if order_number == question.test.questions.count():
            test_result.state = TestResult.STATE.FINISHED
            test_result.score = test_result.num_correct_answers / test_result.test.questions.count() * 100
            test_result.points = max(0, (test_result.num_correct_answers - test_result.num_incorrect_answers))
            test_result.taken_time = test_result.write_date - test_result.create_date
            test_result.save()

            user = User.objects.get(username=request.user)
            current_rating = user.rating
            new_rating = current_rating + test_result.points
            user.rating = new_rating
            user.save()

            return render(
                request=request,
                template_name='finish.html',
                context={
                    'test_result': test_result,
                    'time_finished': test_result.write_date,
                    'points': test_result.points,
                }
            )
        else:
            return redirect(reverse('tests:question', args=(id, order_number+1)))
