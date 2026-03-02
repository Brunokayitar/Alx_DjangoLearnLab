# Advanced API Project

This project is a Django REST Framework (DRF) API for managing books and authors. It demonstrates advanced API concepts including custom serializers, nested relationships, generic views, filtering, searching, ordering, and permissions.

## Models

- **Author**: Represents an author with a `name` field.
- **Book**: Represents a book with `title`, `publication_year`, and a foreign key to `Author`.

## Serializers

- **BookSerializer**: Serializes all fields of the Book model. Includes custom validation to ensure `publication_year` is not in the future.
- **AuthorSerializer**: Serializes the author's name and includes a nested `BookSerializer` to dynamically list all books by that author.

## API Endpoints

All endpoints are prefixed with `/api/`.

### Book CRUD Operations

| Method | URL                         | Description               | Authentication Required |
|--------|-----------------------------|---------------------------|-------------------------|
| GET    | `/books/`                    | List all books            | No                      |
| GET    | `/books/<int:pk>/`           | Retrieve a single book    | No                      |
| POST   | `/books/create/`             | Create a new book         | Yes                     |
| PUT    | `/books/<int:pk>/update/`    | Update an existing book   | Yes                     |
| DELETE | `/books/<int:pk>/delete/`    | Delete a book             | Yes                     |

## Filtering, Searching, and Ordering

The **list endpoint** (`/api/books/`) supports advanced querying:

- **Filtering** by author:  
  `?author=<author_id>`  
  Example: `/api/books/?author=1`

- **Searching** by title or author name (case‑insensitive partial matches):  
  `?search=<keyword>`  
  Example: `/api/books/?search=django`

- **Ordering** by `title` or `publication_year` (prefix `-` for descending):  
  `?ordering=<field>`  
  Examples:  
  - `/api/books/?ordering=publication_year` (ascending)  
  - `/api/books/?ordering=-title` (descending)

You can combine these:  
`/api/books/?search=django&ordering=publication_year`

## Permissions

- Read‑only endpoints (`/books/`, `/books/<int:pk>/`) are open to everyone (`AllowAny`).
- Write endpoints (`create`, `update`, `delete`) require authentication (`IsAuthenticated`).  
  Use session authentication (via the browsable API) or token authentication (if configured).

## Testing with curl

**Obtain a token** (if token auth is enabled):
```bash
curl -X POST http://127.0.0.1:8000/api/api-token-auth/ \
     -H "Content-Type: application/json" \
     -d '{"username":"your_username","password":"your_password"}'
