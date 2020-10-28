from accounts.models import User

from core.models import BaseModel

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class Test(models.Model):
    QUESTION_MIN_LIMIT = 3
    QUESTION_MAX_LIMIT = 20

    class LEVEL_CHOICES(models.IntegerChoices):
        BASIC = 0, "Basic"
        MIDDLE = 1, "Middle"
        ADVANCED = 2, "Advanced"

    topic = models.ForeignKey(to=Topic, related_name='tests', null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, null=True, blank=True)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES.choices, default=LEVEL_CHOICES.MIDDLE)
    image = models.ImageField(default='default.png', upload_to='covers')

    def __str__(self):
        return f'{self.title}'


class Question(models.Model):
    ANSWER_MIN_LIMIT = 3
    ANSWER_MAX_LIMIT = 6

    test = models.ForeignKey(to=Test, related_name='questions', on_delete=models.CASCADE)
    order_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(Test.QUESTION_MAX_LIMIT)])
    text = models.CharField(max_length=64)
    description = models.TextField(max_length=512, null=True, blank=True)

    def __str__(self):
        return f'{self.text}'


class Answer(models.Model):
    text = models.CharField(max_length=64)
    question = models.ForeignKey(to=Question, related_name='answers', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text}'


class TestResult(BaseModel):
    class STATE(models.IntegerChoices):
        NEW = 0, "New"
        FINISHED = 1, "Finished"

    user = models.ForeignKey(to=User, related_name='test_results', on_delete=models.CASCADE)
    test = models.ForeignKey(to=Test, related_name='test_results', on_delete=models.CASCADE)
    state = models.PositiveSmallIntegerField(default=STATE.NEW, choices=STATE.choices)
    num_correct_answers = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(Test.QUESTION_MAX_LIMIT)]
    )
    num_incorrect_answers = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(Test.QUESTION_MAX_LIMIT)]
    )
    current_order_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(Test.QUESTION_MAX_LIMIT)])

    def __str__(self):
        return f'{self.test} ran by {self.user.full_name()} at {self.write_date}'

    def points(self):
        return max(0, self.num_correct_answers - self.num_incorrect_answers)

    def time_spent(self):
        return self.write_date - self.create_date

    def score(self):
        return (self.num_correct_answers / self.test.questions.count()) * 100

    @classmethod
    def current_unfinished_run(cls, user, test_id):
        qs = cls.objects.filter(
            user=user,
            state=cls.STATE.NEW,
            test=test_id,
        )
        return qs.first() if qs.count() else None

    @staticmethod
    def best_result(test_id):
        queryset = TestResult.objects.filter(test=test_id)
        if queryset.count() > 0:
            obj = queryset.extra(select={
                'points': 'num_correct_answers - num_incorrect_answers', 'duration': 'write_date - create_date'},
                order_by=['-points', 'duration'])[0]
            result = f'{obj.user} scored {obj.num_correct_answers} points'
            return result
        else:
            result = 'No one has done this test yet'
            return result

    @staticmethod
    def last_run(test_id):
        if TestResult.objects.filter(test=test_id).count() > 0:
            ob = TestResult.objects.filter(test=test_id).order_by('-write_date').first()
            result = ob.write_date
            return result
        else:
            result = 'No one has run this test yet'
            return result
