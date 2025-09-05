# relationship_app/query_samples.py
import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')  # Replace with your actual project name

django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def query_all_books_by_author(author_name):
    """
    Query all books by a specific author
    """
    try:
        # Use filter() instead of get() to handle multiple authors with same name
        authors = Author.objects.filter(name=author_name)
        if not authors.exists():
            print(f"Author '{author_name}' not found.")
            return []
        
        print(f"Books by {author_name}:")
        all_books = []
        for author in authors:
            books = author.books.all()
            for book in books:
                print(f"- {book.title}")
                all_books.append(book)
        
        return all_books
    except Exception as e:
        print(f"Error querying books by author: {e}")
        return []

def list_all_books_in_library(library_name):
    """
    List all books in a library
    """
    try:
        libraries = Library.objects.filter(name=library_name)
        if not libraries.exists():
            print(f"Library '{library_name}' not found.")
            return []
        
        all_books = []
        for library in libraries:
            books = library.books.all()
            print(f"Books in {library_name} library:")
            for book in books:
                print(f"- {book.title} by {book.author.name}")
                all_books.append(book)
        
        return all_books
    except Exception as e:
        print(f"Error listing books in library: {e}")
        return []

def retrieve_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library
    """
    try:
        libraries = Library.objects.filter(name=library_name)
        if not libraries.exists():
            print(f"Library '{library_name}' not found.")
            return None
        
        for library in libraries:
            try:
                librarian = library.librarian
                print(f"Librarian for {library_name}: {librarian.name}")
                return librarian
            except Librarian.DoesNotExist:
                print(f"No librarian found for {library_name}.")
                continue
        
        return None
    except Exception as e:
        print(f"Error retrieving librarian: {e}")
        return None

def clear_existing_data():
    """
    Clear existing data to avoid duplicates
    """
    Librarian.objects.all().delete()
    Library.objects.all().delete()
    Book.objects.all().delete()
    Author.objects.all().delete()
    print("Existing data cleared.")

def create_sample_data():
    """
    Create sample data for testing the queries
    """
    # Clear existing data first
    clear_existing_data()
    
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George R.R. Martin")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
    book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)
    book3 = Book.objects.create(title="A Game of Thrones", author=author2)
    book4 = Book.objects.create(title="A Clash of Kings", author=author2)
    
    # Create libraries
    library1 = Library.objects.create(name="Central Library")
    library2 = Library.objects.create(name="City Library")
    
    # Add books to libraries
    library1.books.add(book1, book2, book3)
    library2.books.add(book3, book4)
    
    # Create librarians
    Librarian.objects.create(name="Alice Johnson", library=library1)
    Librarian.objects.create(name="Bob Smith", library=library2)
    
    print("Sample data created successfully!")

def demonstrate_queries():
    """
    Demonstrate all the required queries
    """
    print("="*60)
    print("DEMONSTRATING RELATIONSHIP QUERIES")
    print("="*60)
    
    # 1. Query all books by a specific author
    print("\n1. Query all books by a specific author:")
    print("-" * 40)
    query_all_books_by_author("J.K. Rowling")
    
    # 2. List all books in a library
    print("\n2. List all books in a library:")
    print("-" * 40)
    list_all_books_in_library("Central Library")
    
    # 3. Retrieve the librarian for a library
    print("\n3. Retrieve the librarian for a library:")
    print("-" * 40)
    retrieve_librarian_for_library("Central Library")
    
    # Additional examples
    print("\n" + "="*60)
    print("ADDITIONAL EXAMPLES")
    print("="*60)
    
    query_all_books_by_author("George R.R. Martin")
    print()
    list_all_books_in_library("City Library")
    print()
    retrieve_librarian_for_library("City Library")

if __name__ == "__main__":
    # Create sample data first
    create_sample_data()
    
    # Demonstrate the queries
    demonstrate_queries()
