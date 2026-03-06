# Tagging and Search Features

## Tagging
- Posts can be assigned tags during creation/editing. Enter tags as a comma-separated list (e.g., `django, python, blog`).
- Tags are displayed on post detail and list pages.
- Clicking a tag shows all posts with that tag.

## Search
- A search bar is available in the navigation bar.
- Search queries look in post titles, content, and tag names.
- Results are displayed on a dedicated search results page.

## Implementation
- **Model**: `Tag` with a `name` field; `Post` has a ManyToManyField to `Tag`.
- **Form**: `PostForm` includes a `tags` CharField that is parsed into Tag objects.
- **Views**:
  - `PostByTagListView`: lists posts for a given tag.
  - `search`: handles search queries using Q objects.
- **URLs**:
  - `/tags/<tag_name>/` – posts by tag
  - `/search/` – search results

## Usage
1. When creating/editing a post, enter tags separated by commas.
2. Tags appear as links below the post title.
3. Use the search bar at the top right to find posts.
