## 2026-09-05 - Django Post Listing Query Optimization (N+1 Prevention)
**Learning:** Post querysets in `home` and `PostListView` were triggering separate SQL queries for each post's author, category, and tags during template rendering, leading to 34+ database queries per request. Adding `select_related('author', 'category')` and `prefetch_related('tags')` reduces database queries on the homepage to 13 (a ~62% query reduction).
**Action:** Always inspect template renderings of object lists in Django for missing `select_related` and `prefetch_related` calls on foreign keys and M2M fields.
