from bookshelf.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
def books_by_author(author_name):
    try:
        # 1. Get the author object by name
        author = Author.objects.get(name=author_name)
        # 2. Get all books written by this author
        return Book.objects.filter(author=author)
    except Author.DoesNotExist:
        return Book.objects.none()

# 2. List all books in a library
def books_in_library(library_name):
    return Library.objects.get(name=library_name).books.all()

# 3. Retrieve the librarian for a library
def librarian_for_library(library_name):
    try:
        # Get the library object by name
        library = Library.objects.get(name=library_name)
        # Get the librarian assigned to this library
        return Librarian.objects.get(library=library)
    except Library.DoesNotExist:
        return None  # Library not found
    except Librarian.DoesNotExist:
        return None  # Librarian not found for this library