from django.urls import path
from . import views

urlpatterns = [
    # List all books / Create new book
    path('books/', views.BookListCreateView.as_view(), name='book-list-create'),

    # Retrieve, update, delete single book
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
]
