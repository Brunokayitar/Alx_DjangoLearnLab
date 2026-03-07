# Task Management API

A Django REST Framework API for managing tasks. Users can create, update, delete, and mark tasks complete/incomplete. Tasks are private to each user.

## Features
- User registration and token authentication
- CRUD for tasks
- Mark tasks as complete/incomplete (with timestamp)
- Filtering by status, priority, due date
- Sorting by due date, priority, created_at
- Pagination (20 per page)
- Validation: due date must be future, completed tasks cannot be edited

## Endpoints

### Users
- `POST /api/users/` – Register a new user  
  Request: `{"username": "...", "email": "...", "password": "...", "password2": "..."}`  
  Returns: user data and token (token is included in response? Actually token is obtained via login.)
- `POST /api/auth/login/` – Obtain token  
  Request: `{"username": "...", "password": "..."}`  
  Returns: token
- `GET /api/users/` – List users (staff only, else only yourself)
- `GET /api/users/<id>/` – Retrieve a user (staff or yourself)
- `PUT/PATCH /api/users/<id>/` – Update user (staff or yourself)
- `DELETE /api/users/<id>/` – Delete user (staff or yourself)

### Tasks
All task endpoints require token authentication (`Authorization: Token <token>`).

- `GET /api/tasks/` – List your tasks (supports filtering and ordering)
- `POST /api/tasks/` – Create a new task  
  Request: `{"title": "...", "description": "...", "due_date": "YYYY-MM-DD", "priority": "L|M|H"}`
- `GET /api/tasks/<id>/` – Retrieve a task
- `PUT/PATCH /api/tasks/<id>/` – Update a task
- `DELETE /api/tasks/<id>/` – Delete a task
- `POST /api/tasks/<id>/mark-complete/` – Mark task as complete
- `POST /api/tasks/<id>/mark-incomplete/` – Revert task to incomplete

### Filtering & Ordering
- `?status=P` or `?status=C`
- `?priority=L` or `?priority=M` or `?priority=H`
- `?due_date=YYYY-MM-DD`
- `?ordering=due_date`, `?ordering=-due_date`, `?ordering=priority`, `?ordering=created_at`

## Deployment
This API is configured for Heroku. Set environment variables:
- `SECRET_KEY`
- `DEBUG` (False in production)
- `ALLOWED_HOSTS` (comma-separated)
- `DATABASE_URL` (automatically set by Heroku)

## Local Setup
1. Clone repo
2. `python -m venv venv`
3. `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
4. `pip install -r requirements.txt`
5. `python manage.py migrate`
6. `python manage.py runserver`
