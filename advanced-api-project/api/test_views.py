from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from .models import Author, Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username="tester", password="pass1234")

        # Create an author and a few books
        self.author = Author.objects.create(name="John Doe")
        self.book1 = Book.objects.create(
            title="Django Basics", publication_year=2020, author=self.author
        )
        self.book2 = Book.objects.create(
            title="Advanced Django", publication_year=2023, author=self.author
        )

        # Endpoints
        self.list_url = reverse("book-list")
        self.create_url = reverse("book-create")
        self.detail_url = reverse("book-detail", args=[self.book1.id])
        self.update_url = reverse("book-update", args=[self.book1.id])
        self.delete_url = reverse("book-delete", args=[self.book1.id])

    # -------------------
    # CRUD TESTS
    # -------------------
    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Django Basics")

    def test_create_book_requires_authentication(self):
        data = {"title": "New Book", "publication_year": 2024, "author": self.author.id}
        # Unauthenticated request
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated request
        self.client.login(username="tester", password="pass1234")
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book(self):
        self.client.login(username="tester", password="pass1234")
        data = {"title": "Updated Django", "publication_year": 2021, "author": self.author.id}
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Django")

    def test_delete_book(self):
        self.client.login(username="tester", password="pass1234")
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # -------------------
    # FILTERING, SEARCHING, ORDERING TESTS
    # -------------------
    def test_filter_books_by_publication_year(self):
        response = self.client.get(f"{self.list_url}?publication_year=2020")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Django Basics")

    def test_search_books_by_title(self):
        response = self.client.get(f"{self.list_url}?search=Advanced")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Advanced Django")

    def test_order_books_by_publication_year_descending(self):
        response = self.client.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Advanced Django")
