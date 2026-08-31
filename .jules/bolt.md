## 2026-08-31 - Eliminate N+1 queries on homepage with select_related and prefetch_related
**Learning:** Blog home page views fetching featured posts and paginated post lists trigger N+1 database queries when accessing foreign keys (`author`, `category`) and many-to-many relationships (`tags`) in the Django template.
**Action:** Always use `.select_related('author', 'category')` and `.prefetch_related('tags')` on index list view querysets that render relational data per post.
