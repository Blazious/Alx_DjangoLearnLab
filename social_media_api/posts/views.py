from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes


try:
    from notifications.utils import create_notification
except Exception:
    # if notifications app missing or during tests, fallback to no-op
    def create_notification(*args, **kwargs):
        return None


class FeedPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Optional custom paginator
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    # ✅ explicit Post.objects.all() 
    queryset = Post.objects.all()
    # optional optimization preserved
    queryset = Post.objects.select_related('author').prefetch_related('comments')
    
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    # ✅ explicit Comment.objects.all() f
    queryset = Comment.objects.all()
    # optional optimization preserved
    queryset = Comment.objects.select_related('author', 'post')

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        # Create notification for the post author (comment notification)
        if comment.post.author != self.request.user:
            create_notification(
                recipient=comment.post.author,
                actor=self.request.user,
                verb='commented on',
                target=comment,
            )


class FeedListView(generics.ListAPIView):
    """
    Returns posts from users the current user follows, ordered by newest first.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = FeedPagination

    def get_queryset(self):
        user = self.request.user
        # Get users the current user follows
        following_users = user.following.all()
        # Return posts from those users ordered by creation date
        return Post.objects.filter(author__in=following_users).order_by('-created_at') \
    .select_related('author').prefetch_related('comments')

class LikeView(generics.GenericAPIView):
    """
    POST /api/posts/<pk>/like/   -> like the post
    DELETE /api/posts/<pk>/like/ -> unlike the post
    """
    queryset = Post.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        # prevent duplicate likes due to unique_together, but return friendly message
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            # create notification for post owner (if not liking own post)
            if post.author != request.user:
                create_notification(
                    recipient=post.author,
                    actor=request.user,
                    verb='liked',
                    target=post,
                )
            return Response({'detail': 'Post liked.'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Already liked.'}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
        # Optionally: also remove notification (could be left as history)
        return Response({'detail': 'Like removed.'}, status=status.HTTP_200_OK)