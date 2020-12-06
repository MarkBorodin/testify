from django.forms.models import inlineformset_factory

from testify.forms import AnswerAdminForm, AnswersInlineFormSet, QuestionForm, QuestionsInlineFormSet
from testify.models import Answer, Question, Test
from testify.tests.test_base import TestCaseBase


class AdminQuestionsInlineFormSetTest(TestCaseBase):
    fixtures = [
        'tests/fixtures/dump.json',
    ]

    def setUp(self):
        self.test = Test.objects.first()

        self.QuestionFormSet = inlineformset_factory(
            Test, Question, QuestionForm, formset=QuestionsInlineFormSet)

        self.data = {
            'questions-INITIAL_FORMS': 0,
            'questions-MAX_NUM_FORMS': 1000,
            'questions-TOTAL_FORMS': 3,
            'questions-0-text': '2+2',
            'questions-0-order_number': '1',
            'questions-1-text': '3+3',
            'questions-1-order_number': '2',
            'questions-2-text': '4+4',
            'questions-2-order_number': '3',
        }

    def test_formset_is_valid_if_questions_number_is_in_range(self):
        formset = self.QuestionFormSet(self.data, instance=self.test)
        self.assertEqual(formset.is_valid(), True)

    def test_formset_is_invalid_if_questions_number_is_out_of_range_max(self):
        self.data['questions-TOTAL_FORMS'] = Test.QUESTION_MAX_LIMIT + 1
        formset = self.QuestionFormSet(self.data, instance=self.test)
        self.assertEqual(formset.is_valid(), False)

    def test_formset_is_invalid_if_questions_number_is_out_of_range_min(self):
        self.data['questions-TOTAL_FORMS'] = Test.QUESTION_MIN_LIMIT - 1
        formset = self.QuestionFormSet(self.data, instance=self.test)
        self.assertEqual(formset.is_valid(), False)

    def test_formset_is_invalid_if_order_number_is_incorrect(self):
        self.data['questions-2-order_number'] = '12'
        formset = self.QuestionFormSet(self.data, instance=self.test)
        self.assertEqual(formset.is_valid(), False)

        self.data['questions-2-order_number'] = self.data['questions-1-order_number']
        formset = self.QuestionFormSet(self.data, instance=self.test)
        self.assertEqual(formset.is_valid(), False)

        # self.data['questions-2-order_number'] = '-1'
        # formset = self.QuestionFormSet(self.data, instance=self.test)
        # self.assertEqual(formset.is_valid(), False)


class AdminAnswerInlineFormSetTest(TestCaseBase):
    fixtures = [
        'tests/fixtures/dump.json',
    ]

    def setUp(self):
        self.question = Question.objects.get(id=1)

        self.AnswerFormSet = inlineformset_factory(
            Question, Answer, AnswerAdminForm, formset=AnswersInlineFormSet)

        self.data = {
            'answers-INITIAL_FORMS': 0,
            'answers-MAX_NUM_FORMS': 1000,
            'answers-MIN_NUM_FORMS': 0,
            'answers-TOTAL_FORMS': 4,
            'answers-0-text': '4',
            'answers-0-is_correct': 'on',
            'answers-1-text': '5',
            'answers-2-text': '6',
            'answers-3-text': '7',
        }

    def test_formset_is_valid_if_is_correct_in_answers(self):
        formset = self.AnswerFormSet(self.data, instance=self.question)
        self.assertEqual(formset.is_valid(), True)

    def test_formset_is_invalid_if_not_is_correct_in_answers(self):
        self.data['answers-0-is_correct'] = ''
        formset = self.AnswerFormSet(self.data, instance=self.question)
        self.assertEqual(formset.is_valid(), False)

    def test_formset_is_invalid_if_all_is_correct_in_answers(self):
        self.data['answers-0-is_correct'] = 'on'
        self.data['answers-1-is_correct'] = 'on'
        self.data['answers-2-is_correct'] = 'on'
        self.data['answers-3-is_correct'] = 'on'
        formset = self.AnswerFormSet(self.data, instance=self.question)
        self.assertEqual(formset.is_valid(), False)

    def test_formset_is_valid_if_answers_number_is_in_range(self):
        if Question.ANSWER_MIN_LIMIT > self.data['answers-TOTAL_FORMS'] < Question.ANSWER_MAX_LIMIT:
            formset = self.AnswerFormSet(self.data, instance=self.question)
            self.assertEqual(formset.is_valid(), True)

    def test_formset_is_invalid_if_answers_number_is_out_of_range_max(self):
        self.data['answers-TOTAL_FORMS'] = Question.ANSWER_MAX_LIMIT + 1
        formset = self.AnswerFormSet(self.data, instance=self.question)
        self.assertEqual(formset.is_valid(), False)

    def test_formset_is_invalid_if_answers_number_is_out_of_range_min(self):
        self.data['answers-TOTAL_FORMS'] = Question.ANSWER_MIN_LIMIT - 1
        formset = self.AnswerFormSet(self.data, instance=self.question)
        self.assertEqual(formset.is_valid(), False)
