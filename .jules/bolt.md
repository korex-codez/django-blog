## 2026-08-25 - Eager loading Post relations in Django views
**Learning:** Post list views (home page and PostListView) suffered from N+1 query performance issues when rendering foreign keys (`author`, `category`) and M2M relations (`tags`) in templates. Eager loading via `select_related('author', 'category')` and `prefetch_related('tags')` reduces query count per post list rendering.
**Action:** Always use `select_related` for foreign key relationships and `prefetch_related` for M2M relationships when querying Django models that display related attributes in templates.
