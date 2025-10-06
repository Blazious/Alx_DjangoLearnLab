from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    FollowUnfollowAPIView,
    FollowingListView,
    FollowersListView,
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # follow / unfollow (explicit for checker)
    path('follow/<int:user_id>/', FollowUnfollowAPIView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', FollowUnfollowAPIView.as_view(), name='unfollow-user'),

    # lists
    path('<int:user_id>/following/', FollowingListView.as_view(), name='following-list'),
    path('<int:user_id>/followers/', FollowersListView.as_view(), name='followers-list'),
]
