from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, Textarea

from .models import Client, Comment, Contact, Lessons, Post


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
            "whose",
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

    class Meta:
        model = Lessons
        fields = ["client", "date", "price", "whose", "was"]


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "phone", "email", "level"]
        widgets = {
            "name": TextInput(
                attrs={"class": "form-control", "placeholder": "Введите Ваше имя"}
            ),
            "phone": TextInput(
                attrs={"class": "form-control", "placeholder": "Введите Ваш телефон"}
            ),
            "email": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите адрес Вашей электронной почты",
                }
            ),
        }


class AuthUserForm(AuthenticationForm, ModelForm):
    class Meta:
        model = User
        fields = ("username", "password")
        widgets = {
            "username": TextInput(
                attrs={"class": "form-control", "placeholder": "Введите ваш логин"}
            ),
            "password": TextInput(
                attrs={"class": "form-control", "placeholder": "Введите пароль"}
            ),
        }


class RegisterUserForm(ModelForm):
    class Meta:
        model = User
        fields = ("username", "password", "email")
        widgets = {
            "username": TextInput(
                attrs={"class": "form-control", "placeholder": "Придумайте логин"}
            ),
            "password": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Не более 150 символов. Только буквы, цифры и символы @/./+/-/_",
                }
            ),
            "email": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите адрес Вашей электронной почты",
                }
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
