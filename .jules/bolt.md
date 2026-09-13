## 2026-09-13 - ORM N+1 Query Optimization in Django Views
**Learning:** Accessing foreign key relationships (`post.author`, `post.category`) and many-to-many fields (`post.tags`) in Django template loops triggers separate DB queries for each item if not preloaded. Using `select_related('author', 'category')` for single relationships and `prefetch_related('tags')` for many-to-many relationships reduces database queries on post list views by ~75-80%.
**Action:** Always include `select_related` and `prefetch_related` on querysets rendered in list templates that access related fields.
