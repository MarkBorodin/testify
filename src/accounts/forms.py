from accounts.models import User

from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm, UserCreationForm
from django.forms import Form, fields


class AccountCreateForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ['username', 'password1', 'password2', 'email']


class AccountUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'image']


class AccountPasswordChangeForm(PasswordChangeForm):
    pass


class ContactUs(Form):
    subject = fields.CharField(max_length=256, empty_value='Message from Testify')
    message = fields.CharField()


class TrialLesson(Form):
    name = fields.CharField(max_length=64)
    phone_number = fields.CharField(max_length=64)
    level = fields.CharField(max_length=64)
    email = fields.CharField(max_length=64)
