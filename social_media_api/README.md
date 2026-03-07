# Social Media API

This is a Django REST Framework based API for a social media platform.

## Features (Task 0)
- Custom user model with `bio`, `profile_picture`, and `followers` (self-referential many-to-many).
- Token authentication.
- Endpoints:
  - `POST /api/accounts/register/` – register a new user, returns token.
  - `POST /api/accounts/login/` – log in, returns token.
  - `GET /api/accounts/profile/` – retrieve/update own profile (requires token).

## Setup
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
4. Install dependencies: `pip install django djangorestframework`
5. Run migrations: `python manage.py migrate`
6. Start server: `python manage.py runserver`

## Testing
Use Postman or curl to test endpoints as described above.
