from rest_framework import viewsets, permissions, filters, generics
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly



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
        serializer.save(author=self.request.user)


class FeedListView(generics.ListAPIView):
    """
    Returns posts from users the current user follows, ordered by newest first.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = FeedPagination

    def get_queryset(self):
        user = self.request.user
        # authors the user follows; include user's own posts optionally:
        following_qs = user.following.all()
        # include own posts, uncomment next line if you want to include user's posts:
        # authors = list(following_qs) + [user]
        authors = following_qs
        # filter posts by those authors, order desc
        return Post.objects.filter(author__in=authors).select_related('author').prefetch_related('comments').order_by('-created_at')
