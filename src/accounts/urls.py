from accounts.views import AccountCreateView, AccountListView, AccountLoginView, AccountLogoutView, \
    AccountPasswordChangeView, AccountUpdateView, LeaderboardListView

from django.urls import path


app_name = 'accounts'

urlpatterns = [
    path('', AccountListView.as_view(), name='users'),
    path('register/', AccountCreateView.as_view(), name='register'),
    path('login/', AccountLoginView.as_view(), name='login'),
    path('logout/', AccountLogoutView.as_view(), name='logout'),
    path('profile/', AccountUpdateView.as_view(), name='profile'),
    path('password/', AccountPasswordChangeView.as_view(), name='password'),
    path('leaderboard/', LeaderboardListView.as_view(), name='leaderboard'),
    ]
