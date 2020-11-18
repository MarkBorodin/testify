from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from testify.forms import AnswerFormSet
from testify.models import Question, Test, TestResult, UserResponse


class TestListView(LoginRequiredMixin, ListView):
    model = Test
    template_name = 'list.html'
    context_object_name = 'tests'


class TestDetailView(LoginRequiredMixin, DetailView):
    model = Test
    template_name = 'details.html'
    context_object_name = 'test'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test_id = self.kwargs['id']
        all_results = TestResult.objects.filter(test=test_id)
        context['all_results'] = all_results
        context['best_result'] = TestResult.best_result(test_id)
        context['last_run'] = TestResult.last_run(test_id)
        context['current_unfinished_run'] = TestResult.current_unfinished_run(
            user=self.request.user,
            test_id=test_id,
        )
        return context


class TestRunnerView(LoginRequiredMixin, View):

    def get(self, request, id):  # noqa
        TestResult.objects.get_or_create(
            user=request.user,
            state=TestResult.STATE.NEW,
            test=Test.objects.get(id=id),
            defaults=dict(
                current_order_number=1
            )
        )

        return redirect(reverse('tests:next', args=(id, )))


class QuestionView(LoginRequiredMixin, View):

    def get(self, request, id):  # noqa
        test_result = TestResult.objects.filter(
            user=request.user,
            state=TestResult.STATE.NEW,
            test=Test.objects.get(id=id),
        )

        if test_result.count() == 0:
            return redirect(reverse('tests:details', args=(id,)))

        test_result = test_result.first()

        order_number = test_result.current_order_number
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


    def post(self, request, id):  # noqa
        test_result = TestResult.objects.filter(
            user=request.user,
            state=TestResult.STATE.NEW,
            test=Test.objects.get(id=id),
        )

        if test_result.count() == 0:
            return redirect(reverse('tests:details', args=(id,)))

        test_result = test_result.first()

        order_number = test_result.current_order_number
        question = Question.objects.get(test__id=id, order_number=order_number)
        answers = question.answers.all()
        form_set = AnswerFormSet(data=request.POST)

        # for form in form_set:
        #     if 'is_selected' in form.changed_data:
        #         answer = Answer.objects.get(id=form.instance.id)
        #         user_response = UserResponse.objects.create(
        #             test_result=test_result,
        #             question=question,
        #             user_response=answer,
        #         )
        #         user_response.save()

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
        test_result.current_order_number += 1
        test_result.save()

        if order_number == question.test.questions.count():
            test_result.state = TestResult.STATE.FINISHED
            test_result.save()
            user_responses = UserResponse.objects.filter(
                test_result=test_result.id
            )
            questions = Question.objects.filter(
                test=id
            )

            return render(
                request=request,
                template_name='finish.html',
                context={
                    'test_result': test_result,
                    'user_responses': user_responses,
                    'questions': questions,
                }
            )
        else:
            return redirect(reverse('tests:next', args=(id,)))


def error_404(request, exception):
    data = {}
    return render(request, '404.html', data)


def error_500(request,  exception):
    data = {}
    return render(request, '500.html', data)


def error_403(request, exception):
    data = {}
    return render(request, '404.html', data)


def error_400(request,  exception):
    data = {}
    return render(request, '500.html', data)
