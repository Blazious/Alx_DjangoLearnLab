from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


# ✅ List all books / Create a book
class BookListCreateView(generics.ListCreateAPIView):
    """
    Handles:
    - GET /books/ → List all books
    - POST /books/ → Create a new book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Permissions: anyone can view, only authenticated users can create
    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


# ✅ Retrieve / Update / Delete a single book
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles:
    - GET /books/<id>/ → Retrieve a book
    - PUT/PATCH /books/<id>/ → Update a book
    - DELETE /books/<id>/ → Delete a book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Permissions: anyone can view, only authenticated users can update/delete
    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
