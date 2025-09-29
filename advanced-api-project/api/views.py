from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter  # ✅ correct place
from django_filters.rest_framework import DjangoFilterBackend   # ✅ only for filtering

from .models import Book
from .serializers import BookSerializer


# ✅ List all books with filtering, searching, and ordering
class BookListView(generics.ListAPIView):
    """
    GET /books/?title=SomeTitle
    GET /books/?author=1
    GET /books/?publication_year=2023
    GET /books/?search=python
    GET /books/?ordering=title
    GET /books/?ordering=-publication_year
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Filtering, Searching, Ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Filtering by model fields
    filterset_fields = ["title", "author", "publication_year"]

    # Search across fields (partial match)
    search_fields = ["title", "author__name"]

    # Ordering allowed by these fields
    ordering_fields = ["title", "publication_year"]

    # Default ordering (if none specified)
    ordering = ["title"]


# ✅ Create a new book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# ✅ Retrieve a single book
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ✅ Update a book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# ✅ Delete a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
