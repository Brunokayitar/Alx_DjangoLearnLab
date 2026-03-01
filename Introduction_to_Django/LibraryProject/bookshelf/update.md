# Update Operation

```python
from bookshelf.models import Book

# Retrieve and update the book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated title: {book.title}")
```

**Expected Output:**

```
Updated title: Nineteen Eighty-Four
```
