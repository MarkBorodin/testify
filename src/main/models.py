from datetime import datetime

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


class Contact(BaseModel):
    name = models.CharField("Имя", max_length=64)
    phone = models.CharField("Телефон", max_length=24)
    email = models.EmailField("Почта")
    level = models.ForeignKey(to=Level, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class Whose(models.Model):
    owner = models.CharField("Чей клиент", max_length=64)

    def __str__(self):
        return self.owner

    class Meta:
        verbose_name = "Чей ученик"
        verbose_name_plural = "Чии ученики"


class Client(BaseModel):
    firstname = models.CharField("Имя", max_length=64)
    lastname = models.CharField("Фамилия", max_length=64)
    phone = models.CharField("Телефон", max_length=24)
    email = models.EmailField("Почта")
    age = models.IntegerField("Возраст")
    skype = models.CharField("Skype", max_length=124)
    level = models.ForeignKey(to=Level, on_delete=models.CASCADE)
    whose = models.ForeignKey(to=Whose, on_delete=models.CASCADE)

    def __str__(self):
        return self.firstname

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Lessons(BaseModel):
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    date = models.DateTimeField("Дата", null=True, blank=True)
    price = models.IntegerField("Цена")
    whose = models.ForeignKey(Whose, on_delete=models.CASCADE)
    was = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"
        ordering = ["date"]

    def __str__(self):
        return str(self.client)

    @classmethod
    def get_this_month_income(cls):
        current_month = datetime.now().month
        current_year = datetime.now().year
        this_month_lessons = cls.objects.filter(date__month=current_month, date__year=current_year)
        month_income = 0
        for lesson in this_month_lessons:
            month_income += lesson.price
        return month_income

    @classmethod
    def get_this_day_income(cls):
        current_day = datetime.now().day
        current_month = datetime.now().month
        current_year = datetime.now().year
        today_income = 0
        this_day_income = cls.objects.filter(date__month=current_month, date__year=current_year, date__day=current_day)
        for lesson in this_day_income:
            today_income += lesson.price
        return today_income
