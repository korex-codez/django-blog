## 2026-08-26 - Eliminate N+1 Database Queries on Home View & Post ListView
**Learning:** Rendering list views containing ForeignKeys (`author`, `category`) and ManyToMany fields (`tags`) without `select_related` and `prefetch_related` causes an N+1 query explosion per post card rendered in Django templates.
**Action:** Always inspect template attribute accesses on model instances (e.g., `post.author.username`, `post.category.name`, `post.tags.all`) and apply `.select_related()` for single relations and `.prefetch_related()` for m2m relations in querysets.
