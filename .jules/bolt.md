## 2026-09-06 - Django Query Optimization in Home View

**Learning:** When rendering lists of model instances (such as posts) that display author details, category info, tags, and M2M counts (like likes count), unoptimized querysets cause N+1 database queries for every rendered item. Using `select_related('author', 'category')`, `prefetch_related('tags')`, and `annotate(like_count=Count('likes', distinct=True))` reduces queries from ~35 down to 6 on page load. Model helper methods like `total_likes()` can check `hasattr(self, 'like_count')` to use the precomputed value seamlessly.
**Action:** Always check template rendering loops for foreign key and M2M attribute accesses and use `select_related`, `prefetch_related`, and `annotate` to batch or precompute data in a single SQL query.
