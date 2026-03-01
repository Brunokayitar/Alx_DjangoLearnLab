# Retrieve Operation

```python
from bookshelf.models import Book

# Retrieve all books
books = Book.objects.all()
for book in books:
    print(f"Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")

# Or retrieve the specific book
book = Book.objects.get(title="1984")
print(f"Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")
```

**Expected Output:**

```
Title: 1984, Author: George Orwell, Year: 1949
```
