from datetime import datetime, timedelta

from accounts.models import User

from core.models import BaseModel
from core.utils import resize_image_for_post

from django.db import models


class Post(BaseModel):
    title = models.CharField("Название", max_length=128)
    content = models.TextField("Контент")
    image = models.ImageField(upload_to='pics/', default='pics/fi1.jpg')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        resize_image_for_post(self.image)
        return result

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-create_date"]


class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField("Комментарий", max_length=256)
    comment_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.comment_text

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["create_date"]


class Level(models.Model):
    level = models.CharField("Уровень", max_length=8)

    def __str__(self):
        return self.level

    class Meta:
        verbose_name = "Уровень"
        verbose_name_plural = "Уровни"


class Client(BaseModel):
    firstname = models.CharField("Имя", max_length=64)
    lastname = models.CharField("Фамилия", max_length=64)
    phone = models.CharField("Телефон", max_length=24)
    email = models.EmailField("Почта", max_length=48)
    age = models.SmallIntegerField("Возраст", null=True)
    skype = models.CharField("Skype", max_length=124, null=True)
    level = models.ForeignKey(to=Level, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        to=User, null=False, blank=False, default=11, on_delete=models.SET_DEFAULT, related_name='clients'
    )

    def __str__(self):
        return self.firstname

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Lessons(BaseModel):
    teacher = models.ForeignKey(
        to=User, null=False, blank=False, default=11, on_delete=models.SET_DEFAULT, related_name='lessons'
    )
    client = models.ForeignKey(
        to=Client, null=False, blank=False, default=11, on_delete=models.SET_DEFAULT, related_name='lessons'
    )
    date = models.DateTimeField("Дата", null=True, blank=True)
    price = models.IntegerField("Цена")
    was = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"
        ordering = ["date"]

    def __str__(self):
        return str(self.client)

    @classmethod
    def get_this_month_income(cls, *args):
        current_month = datetime.now().month
        current_year = datetime.now().year
        if args:
            this_month_lessons = cls.objects.filter(date__month=current_month, date__year=current_year, teacher=args[0])
        else:
            this_month_lessons = cls.objects.filter(date__month=current_month, date__year=current_year)
        month_income = 0
        for lesson in this_month_lessons:
            month_income += lesson.price
        return month_income

    @classmethod
    def get_this_day_income(cls, *args):
        current_day = datetime.now().day
        current_month = datetime.now().month
        current_year = datetime.now().year
        if args:
            this_day_income = cls.objects.filter(date__month=current_month, date__year=current_year,
                                                 date__day=current_day, teacher=args[0])
        else:
            this_day_income = cls.objects.filter(date__month=current_month, date__year=current_year,
                                                 date__day=current_day)
        today_income = 0
        for lesson in this_day_income:
            today_income += lesson.price
        return today_income

    @classmethod
    def get_this_week_lessons(cls, user):
        days = [
            (1, 'sunday'), (2, 'monday'), (3, 'tuesday'), (4, 'wednesday'),
            (5, 'thursday'), (6, 'friday'), (7, 'saturday')
        ]
        querysets = []
        for day, day_of_week in days:
            one_day_lessons = cls.objects.filter(teacher=user,
                                                 date__week_day=day, date__gte=(datetime.now() - timedelta(days=1)),
                                                 date__lte=(datetime.now() + timedelta(days=6))).order_by("date")
            item = {
                'index': day,
                'lessons': one_day_lessons,
                'day_of_week': day_of_week,
            }
            querysets.append(item)
        return querysets
