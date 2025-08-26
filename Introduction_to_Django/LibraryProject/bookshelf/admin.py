from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Columns to show in the list view
    list_display = ('title', 'author', 'publication_year')

    # Filters in the sidebar
    list_filter = ('author', 'publication_year')

    # Enable search by title and author
    search_fields = ('title', 'author')
