from accounts.views import AccountCreateView, AccountLoginView, AccountLogoutView, AccountPasswordChangeView, \
    AccountUpdateView

from django.urls import path


app_name = 'accounts'

urlpatterns = [
    path('register/', AccountCreateView.as_view(), name='register'),
    path('login/', AccountLoginView.as_view(), name='login'),
    path('logout/', AccountLogoutView.as_view(), name='logout'),
    path('profile/', AccountUpdateView.as_view(), name='profile'),
    path('password/', AccountPasswordChangeView.as_view(), name='password'),
    ]
