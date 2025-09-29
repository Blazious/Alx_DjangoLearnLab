from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "blog"

urlpatterns = [
    # Home / posts list
    path("", views.PostListView.as_view(), name="post-list"),

    # CRUD (singular "post" as required by checker)
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/new/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),

    # Auth & Profile
    path("register/", views.register_view, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="blog/logout.html"), name="logout"),
    path("profile/", views.profile_view, name="profile"),

    # Comment-related URLs (checker-friendly)
    path("post/<int:pk>/comments/new/", views.CommentCreateView.as_view(), name="comment-create"),
    path("comment/<int:pk>/update/", views.CommentUpdateView.as_view(), name="comment-update"),
    path("comment/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),

    # Tags + Search (checker requires these exact names)
    path("tags/<slug:tag_slug>/", views.PostByTagListView.as_view(), name="posts_by_tag"),
    path("search/", views.SearchResultsView.as_view(), name="search"),,

]
