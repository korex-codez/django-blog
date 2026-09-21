## 2026-03-31 - [N+1 Query Optimization in Post List Views]
**Learning:** Post listing views in Django rendering relations like `post.author.username`, `post.category.name`, `post.tags.all`, and `post.total_likes` incur $O(N)$ database queries unless `select_related('author', 'category')` and `prefetch_related('tags', 'likes')` are explicitly applied on the QuerySet.
**Action:** Always check post list views and templates for accessed relational attributes and attach appropriate `select_related` / `prefetch_related` calls to QuerySets before rendering.
