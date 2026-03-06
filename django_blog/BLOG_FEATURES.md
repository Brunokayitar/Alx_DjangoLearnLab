# Blog Post Management Features

## Overview
This Django blog application provides full CRUD (Create, Read, Update, Delete) functionality for blog posts.

## Features
- **List Posts**: All users (authenticated or not) can view a list of all posts (`/posts/`).
- **View Post**: Anyone can read a full post (`/posts/<id>/`).
- **Create Post**: Authenticated users can create a new post (`/posts/new/`). The author is automatically set to the logged-in user.
- **Edit Post**: Only the author of a post can edit it (`/posts/<id>/edit/`).
- **Delete Post**: Only the author can delete a post (`/posts/<id>/delete/`), with a confirmation page.

## Templates
- `post_list.html` – displays all posts with titles and snippets.
- `post_detail.html` – shows full post content, with edit/delete buttons if user is author.
- `post_form.html` – used for both creating and editing (title and content fields).
- `post_confirm_delete.html` – asks for confirmation before deletion.

## Permissions
- `LoginRequiredMixin` ensures only logged-in users can create, edit, or delete.
- `UserPassesTestMixin` restricts edit/delete to the post's author.

## URL Patterns (in `blog/urls.py`)
- `/posts/` – PostListView
- `/posts/<int:pk>/` – PostDetailView
- `/posts/new/` – PostCreateView
- `/posts/<int:pk>/edit/` – PostUpdateView
- `/posts/<int:pk>/delete/` – PostDeleteView

## Testing
1. Log in with a user.
2. Create a few posts.
3. View the list and individual posts.
4. Edit and delete your own posts.
5. Log in as another user and verify you cannot edit/delete others' posts.
