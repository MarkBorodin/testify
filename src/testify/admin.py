from django.contrib import admin

from testify.forms import AnswersInlineFormSet, QuestionForm, QuestionsInlineFormSet
from testify.models import Answer, Question, Test, TestResult, Topic


class AnswersInline(admin.TabularInline):
    model = Answer
    fields = ('text', 'is_correct')
    show_change_link = True
    formset = AnswersInlineFormSet
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    inlines = (AnswersInline,)
    form = QuestionForm


class QuestionsInline(admin.TabularInline):
    model = Question
    fields = ('text', 'order_number')
    show_change_link = True
    extra = 0
    formset = QuestionsInlineFormSet
    ordering = ('order_number',)


class TestAdmin(admin.ModelAdmin):
    inlines = (QuestionsInline,)


admin.site.register(Topic)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(TestResult)
