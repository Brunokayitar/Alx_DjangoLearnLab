from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book

class BookAPITests(APITestCase):
    def setUp(self):
        # Create a test user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create an author for book relations
        self.author = Author.objects.create(name='Test Author')
        
        # Create some books for testing
        self.book1 = Book.objects.create(
            title='Django for APIs',
            publication_year=2022,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title='Python Crash Course',
            publication_year=2021,
            author=self.author
        )
        
        # URLs for endpoints (adjust if your URL names differ)
        self.list_url = reverse('book-list')           # /api/books/
        self.detail_url = reverse('book-detail', args=[self.book1.id])  # /api/books/<id>/
        self.create_url = reverse('book-create')       # /api/books/create/
        self.update_url = reverse('book-update', args=[self.book1.id])  # /api/books/update/<id>/
        self.delete_url = reverse('book-delete', args=[self.book1.id])  # /api/books/delete/<id>/

    # Helper method for authenticated client
    def authenticate(self):
        self.client.login(username='testuser', password='testpass')

    # --- CRUD Tests ---

    def test_list_books_unauthenticated(self):
        """List view should be accessible without authentication"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two books created

    def test_create_book_unauthenticated(self):
        """Creating a book without authentication should fail"""
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_authenticated(self):
        """Authenticated user should be able to create a book"""
        self.authenticate()
        data = {
            'title': 'Authenticated Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)  # Now 3 books

    def test_detail_book_unauthenticated(self):
        """Detail view should be accessible without authentication"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_update_book_unauthenticated(self):
        """Update without authentication should fail"""
        data = {'title': 'Updated Title'}
        response = self.client.put(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated(self):
        """Authenticated user should be able to update a book"""
        self.authenticate()
        data = {'title': 'Updated Title', 'publication_year': 2022, 'author': self.author.id}
        response = self.client.put(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')

    def test_delete_book_unauthenticated(self):
        """Delete without authentication should fail"""
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_authenticated(self):
        """Authenticated user should be able to delete a book"""
        self.authenticate()
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)  # book1 deleted

    # --- Filtering Tests ---
    def test_filter_by_author(self):
        """Filtering by author ID should return only books by that author"""
        # Create another author with a book
        other_author = Author.objects.create(name='Other Author')
        Book.objects.create(title='Other Book', publication_year=2020, author=other_author)
        
        response = self.client.get(self.list_url, {'author': self.author.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return only books by self.author (2 books)
        self.assertEqual(len(response.data), 2)
        for book in response.data:
            self.assertEqual(book['author'], self.author.id)

    def test_filter_by_title(self):
        """Filtering by title (exact match)"""
        response = self.client.get(self.list_url, {'title': 'Django for APIs'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Django for APIs')

    def test_filter_by_publication_year(self):
        """Filtering by publication year (exact match)"""
        response = self.client.get(self.list_url, {'publication_year': 2021})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 2021)

    # --- Searching Tests ---
    def test_search_by_title(self):
        """Searching by title (partial match)"""
        response = self.client.get(self.list_url, {'search': 'django'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Django for APIs')

    def test_search_by_author_name(self):
        """Searching by author name"""
        response = self.client.get(self.list_url, {'search': 'Test Author'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both books by Test Author

    # --- Ordering Tests ---
    def test_ordering_by_publication_year_asc(self):
        """Order by publication year ascending"""
        response = self.client.get(self.list_url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Years: 2021, 2022
        self.assertEqual(response.data[0]['publication_year'], 2021)
        self.assertEqual(response.data[1]['publication_year'], 2022)

    def test_ordering_by_publication_year_desc(self):
        """Order by publication year descending"""
        response = self.client.get(self.list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2022)
        self.assertEqual(response.data[1]['publication_year'], 2021)

    def test_ordering_by_title_asc(self):
        """Order by title ascending"""
        response = self.client.get(self.list_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item['title'] for item in response.data]
        self.assertEqual(titles, sorted(['Django for APIs', 'Python Crash Course']))