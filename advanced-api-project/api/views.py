from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


# ✅ List all books
class BookListView(generics.ListAPIView):
    """
    GET /books/ → List all books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# ✅ Create a new book
class BookCreateView(generics.CreateAPIView):
    """
    POST /books/ → Create a new book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# ✅ Retrieve a single book
class BookDetailView(generics.RetrieveAPIView):
    """
    GET /books/<id>/ → Retrieve a book by ID
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# ✅ Update a book
class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /books/<id>/ → Update a book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# ✅ Delete a book
class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /books/<id>/ → Delete a book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
