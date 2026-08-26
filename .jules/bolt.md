## 2026-08-26 - Django Queryset N+1 Optimization in List Views
**Learning:** Rendering post cards in template loops (home, post list, search) accesses `post.author`, `post.category`, and `post.tags`. Without eager loading, Django executes N+1 queries for each post card displayed (reducing performance significantly).
**Action:** Use `.select_related('author', 'category')` for foreign keys and `.prefetch_related('tags')` for ManyToMany fields on Django querysets used in list templates.
