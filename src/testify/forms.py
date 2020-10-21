from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, ModelForm

from testify.models import Question


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

    def clean(self):
        pass


class QuestionsInlineFormSet(BaseInlineFormSet):
    def clean(self):
        if not (self.instance.QUESTION_MIN_LIMIT <= len(self.forms) <= self.instance.QUESTION_MAX_LIMIT):
            raise ValidationError('Quantity of question is out of range ({}..{})'.format(
                self.instance.QUESTION_MIN_LIMIT, self.instance.QUESTION_MAX_LIMIT))

        order_number_list = []
        for form in self.forms:
            order_number_list.append(form.cleaned_data['order_number'])

        if 1 not in order_number_list:
            raise ValidationError('Numeration starts with one')

        previous = 1
        for i in sorted(order_number_list)[1:]:
            if i != previous + 1:
                raise ValidationError('All numbers increase with step 1')
            previous = i


class AnswersInlineFormSet(BaseInlineFormSet):
    def clean(self):
        if not (self.instance.ANSWER_MIN_LIMIT <= len(self.forms) <= self.instance.ANSWER_MAX_LIMIT):
            raise ValidationError('Quantity of answer is out of range ({}..{})'.format(
                self.instance.ANSWER_MIN_LIMIT, self.instance.ANSWER_MAX_LIMIT))

        num_correct_answers = sum([
            1
            for form in self.forms
            if form.cleaned_data['is_correct']
        ])

        if num_correct_answers == 0:
            raise ValidationError('At LEAST one answer must be correct!')

        if num_correct_answers == len(self.forms):
            raise ValidationError('Not allowed to select ALL answers!')
