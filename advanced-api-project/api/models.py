from django.db import models

class Author(models.Model):
    """
    Author model representing a book author.
    Each author can have multiple books (one-to-many relationship).
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Book model representing a book with title, publication year, and author.
    Linked to Author via a ForeignKey.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title