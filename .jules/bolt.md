## 2026-09-05 - Django Home View N+1 Query Optimization
**Learning:** In Django template loops displaying posts, accessing `post.author`, `post.category`, and `post.tags` causes N+1 database queries if not explicitly pre-loaded.
**Action:** Always use `.select_related('author', 'category')` and `.prefetch_related('tags')` on Post querysets when rendering post list cards/items in views.
