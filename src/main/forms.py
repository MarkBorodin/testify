from accounts.models import User

from django import forms
from django.forms import ModelForm, TextInput, Textarea

from .models import Client, Comment, Lessons, Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "image"]
        widgets = {
            "title": TextInput(
                attrs={"class": "form-control", "placeholder": "Введите название"}
            ),
            "content": Textarea(
                attrs={"class": "form-control", "placeholder": "Введите описание"}
            ),
        }


class CommentForm(ModelForm):

    comment_text = forms.CharField(
        label="Ваш комментарий",
        widget=forms.widgets.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите комментарий"}
        ),
    )

    class Meta:
        model = Comment
        fields = ["comment_text"]


class ClientForm(ModelForm):
    teacher = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True))

    class Meta:
        model = Client
        fields = [
            "firstname",
            "lastname",
            "phone",
            "email",
            "age",
            "skype",
            "level",
            "teacher",
        ]
        widgets = {
            "firstname": TextInput(
                attrs={"class": "form-control", "placeholder": "Введите имя"}
            ),
            "lastname": TextInput(
                attrs={"class": "form-control", "placeholder": "Введите фамилию"}
            ),
            "age": TextInput(
                attrs={"class": "form-control", "placeholder": "Введите возраст"}
            ),
            "skype": TextInput(
                attrs={"class": "form-control", "placeholder": "Введите скайп"}
            ),
            "phone": TextInput(
                attrs={"class": "form-control", "placeholder": "Введите телефон"}
            ),
            "email": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите адрес электронной почты",
                }
            ),
        }


class LessonsForm(ModelForm):
    date = forms.DateTimeField(input_formats=["%d/%m/%Y %H:%M"])
    teacher = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True))

    class Meta:
        model = Lessons
        fields = ["client", "teacher", "date", "price", "was"]
