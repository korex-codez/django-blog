## 2026-08-25 - Prevent N+1 Database Queries in Django Home Page View
**Learning:** Rendering list views containing relations (such as Post `author`, `category`, and `tags`) without `select_related` and `prefetch_related` causes Django ORM to execute individual database queries per post card rendered in templates, scaling queries to O(N).
**Action:** Always inspect views rendering lists of model instances and apply `.select_related()` for ForeignKey fields and `.prefetch_related()` for ManyToMany fields.
