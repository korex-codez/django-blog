## 2026-09-17 - Optimize Django Post List Views with select_related and prefetch_related
**Learning:** Post list templates render author, category, and tags for every post. Without `select_related('author', 'category')` and `prefetch_related('tags')`, Django triggers separate queries per post card, resulting in 20+ extra SQL queries per request.
**Action:** Always inspect template loops for `post.author`, `post.category`, and `post.tags` in Django views and add `select_related` / `prefetch_related` to post querysets.
