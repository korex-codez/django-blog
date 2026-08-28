## 2026-08-28 - Eager Loading Post Relations
**Learning:** Post list views were incurring N+1 queries when template rendered post cards accessing `post.author`, `post.category`, and `post.tags.all`. Using `select_related('author', 'category')` and `prefetch_related('tags')` reduces query counts per post list page from O(N) to O(1) constant queries.
**Action:** Always inspect template renderings for post listings and apply `select_related` / `prefetch_related` on foreign key and M2M fields.
