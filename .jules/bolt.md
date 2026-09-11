## 2026-03-01 - Django ORM N+1 Queries in Post Card List Rendering
**Learning:** Rendering post cards with author, category, tags, and total likes counts in template loops without `select_related` / `prefetch_related` causes an N+1 query burst (e.g. 27 queries for 4-6 posts on home page).
**Action:** Always wrap Django post querysets passed to card-rendering views with `.select_related('author', 'category').prefetch_related('tags', 'likes')` to keep query count constant at 7 regardless of post list length.
