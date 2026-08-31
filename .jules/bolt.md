## 2026-08-31 - Preloading Foreign Keys and Many-to-Many Relations on Blog Home Views

**Learning:** When Django templates render post lists (such as on the homepage or post list views) containing author information, category badges, and tag badges, iterating over `post.author`, `post.category`, and `post.tags.all()` without prefetching triggers N+1 database queries for every post displayed.

**Action:** Always optimize list views by combining `.select_related('author', 'category')` for foreign key fields and `.prefetch_related('tags')` for M2M fields in Django querysets. In this codebase, this reduced SQL query counts from ~28 down to 3 per page load.
