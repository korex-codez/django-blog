## 2026-09-14 - Optimize Homepage Query Execution with select_related and prefetch_related
**Learning:** Rendering post lists on the homepage without eager loading causes N+1 SQL query overhead for `author`, `category` (foreign keys), and `tags` (many-to-many relationship) across featured and latest post loops.
**Action:** Always combine `select_related('author', 'category')` for single-value FK relations and `prefetch_related('tags')` for M2M relations on any Django list views displaying post meta information to minimize database roundtrips.
