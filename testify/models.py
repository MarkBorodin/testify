from accounts.models import User

from django.db import models


class Test(models.Model):
    test = models.CharField(max_length=128)
    user = models.ManyToManyField(
        to=User,
        null=True,
        related_name='tests',
    )


class Question(models.Model):
    question = models.CharField(max_length=1024)
    correct_answer = models.OneToOneField(
        to=Answer,
        null=False,
        on_delete=models.SET_NULL,
        related_name='questions',
    )
    test = models.ForeignKey(
        to=Test,
        null=False,
        on_delete=models.CASCADE,
        related_name='questions',
    )


class Answer(models.Model):
    answer = models.CharField(max_length=1024)
    question = models.ForeignKey(
        to=Question,
        null=False,
        on_delete=models.CASCADE,
        related_name='answers',
    )


class Result(models.Model):
    correct_answers = models.PositiveSmallIntegerField
    wrong_answers = models.PositiveSmallIntegerField
    percent = models.PositiveSmallIntegerField
    user = models.ForeignKey(
        to=User,
        null=False,
        on_delete=models.CASCADE,
        related_name='results',
    )

    test = models.ForeignKey(
        to=Test,
        null=False,
        on_delete=models.CASCADE,
        related_name='results',
    )
