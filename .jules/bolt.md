## 2026-08-29 - Optimize Home Page Post Queries with select_related and prefetch_related
**Learning:** In Django views rendering post cards (author name, category, tags, total likes), iterating over posts without `select_related('author', 'category')` and `prefetch_related('tags', 'likes')` causes N+1 SQL queries for every post on the page.
**Action:** Always prefetch M2M relations ('tags', 'likes') and select_related FK relations ('author', 'category') when querying posts list for views that render card components.
