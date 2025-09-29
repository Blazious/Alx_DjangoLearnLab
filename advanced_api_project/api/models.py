from django.db import models
from django.utils import timezone


class Author(models.Model):
    """
    Author model
    Represents an author who can have multiple books.
    One-to-many relationship with Book (Author → Books).
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model
    Stores details about a book, including title, publication year,
    and the author who wrote it.
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        related_name="books",  # lets us access author.books.all()
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
