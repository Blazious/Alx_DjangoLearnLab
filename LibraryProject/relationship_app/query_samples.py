from relationship_app.models import Author, Book, Library, Librarian

# Query 1: All books by a specific author
def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    books = author.books.all()  # thanks to related_name="books"
    return books


# Query 2: List all books in a library
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    return books


# Query 3: Retrieve the librarian for a library
def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.librarian


if __name__ == "__main__":
    # Example usage:
    print("Books by J.K. Rowling:")
    for book in books_by_author("J.K. Rowling"):
        print("-", book.title)

    print("\nBooks in Central Library:")
    for book in books_in_library("Central Library"):
        print("-", book.title)

    print("\nLibrarian of Central Library:")
    print(librarian_for_library("Central Library"))
