from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated  
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    permission_classes = [permissions.AllowAny]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['author', 'title', 'publication_year']  
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']

# Retrieve a single book by ID (read-only for everyone)
class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single book by its primary key.
    Accessible to anyone.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

# Create a new book (authenticated users only)
class BookCreateView(generics.CreateAPIView):
    """
    Create a new book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

# Update an existing book (authenticated users only)
class BookUpdateView(generics.UpdateAPIView):
    """
    Update an existing book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

# Delete a book (authenticated users only)
class BookDeleteView(generics.DestroyAPIView):
    """
    Delete a book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]