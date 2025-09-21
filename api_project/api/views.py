from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    API endpoint that allows viewing a list of books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed, created, edited, or deleted.
    Provides full CRUD functionality:
    - list: GET /books_all/
    - retrieve: GET /books_all/{id}/
    - create: POST /books_all/
    - update: PUT /books_all/{id}/
    - partial_update: PATCH /books_all/{id}/
    - delete: DELETE /books_all/{id}/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
