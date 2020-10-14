from accounts.models import User

from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm, UserCreationForm


class AccountCreateForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ['username', 'password1', 'password2']


class AccountUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'image']


class AccountPasswordChangeForm(PasswordChangeForm):
    pass
