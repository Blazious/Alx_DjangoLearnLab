from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "blog"

urlpatterns = [
 # Home / posts list
    path('', views.PostListView.as_view(), name='post-list'),

    # CRUD
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/new/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    

    path("", views.home_view, name="home"),  # if you have a home_view; otherwise adjust
    # Registration
    path("register/", views.register_view, name="register"),
    # Login using Django built-in view (template below must be blog/login.html)
    path("login/", auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    # Logout
    path("logout/", auth_views.LogoutView.as_view(template_name="blog/logout.html"), name="logout"),
    # Profile
    path("profile/", views.profile_view, name="profile"),
]
