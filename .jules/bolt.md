## 2026-09-08 - Home Page N+1 Query Elimination
**Learning:** Home page queries for featured and paginated posts hit the database for author, category, and tags for each individual post card rendered in Django templates.
**Action:** Always use `select_related('author', 'category')` and `prefetch_related('tags')` on Post querysets rendered in list/grid views to reduce queries from ~35 down to 13.
