from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet, CommentViewSet, FeedListView, LikeView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedListView.as_view(), name='feed'),
    path('posts/<int:pk>/like/', LikeView.as_view(), name='post-like'),
]
