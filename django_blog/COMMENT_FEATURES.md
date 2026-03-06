# Comment System Documentation

## Overview
The Django blog now includes a comment system. Users can read comments on each blog post, and authenticated users can add, edit, and delete their own comments.

## Models
- **Comment**: Links to a `Post` and a `User` (author). Fields: `content`, `created_at`, `updated_at`.

## Features
- **View comments**: All comments are displayed on the post detail page, newest first.
- **Add comment**: Authenticated users can post a comment via a form at the bottom of the post detail page.
- **Edit comment**: The author of a comment can edit it by clicking "Edit" next to their comment.
- **Delete comment**: The author can delete their comment after confirmation.

## Permissions
- **Create**: `LoginRequiredMixin` – only logged-in users can access the comment creation form.
- **Update/Delete**: `UserPassesTestMixin` ensures only the comment's author can edit or delete it.

## URL Patterns
- `/posts/<int:post_id>/comments/new/` – create a new comment for a specific post.
- `/comment/<int:pk>/update/` – edit an existing comment.
- `/comment/<int:pk>/delete/` – delete a comment.

## Templates
- `post_detail.html` – extended to show comments and the add form.
- `comment_form.html` – used for both creating and editing comments.
- `comment_confirm_delete.html` – confirmation page before deletion.

## Testing
1. Log in and visit any post detail page.
2. Add a comment – it should appear immediately.
3. Edit your comment – the form pre-fills with existing content.
4. Delete your comment – confirm deletion.
5. Log out – the comment form should be replaced by a login link.
6. Log in as a different user – you should not see edit/delete buttons on others' comments.
