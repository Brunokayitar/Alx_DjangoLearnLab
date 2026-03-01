# Delete Operation

```python
from bookshelf.models import Book

# Delete the book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Verify deletion
all_books = Book.objects.all()
print(f"Books after deletion: {all_books}")
```

**Expected Output:**

```
Books after deletion: <QuerySet []>
```
