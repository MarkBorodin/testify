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

        if self.forms[0].cleaned_data['order_number'] != 1:
            raise ValidationError('Numeration starts with one')

        previous_form = self.forms[0]
        for form in self.forms[1:]:
            if form.cleaned_data['order_number'] != previous_form.cleaned_data['order_number'] + 1:
                raise ValidationError('Numbers must be in correct order')
            previous_form = form


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
