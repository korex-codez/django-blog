## 2026-08-29 - N+1 Query Bottleneck in Home View Post Rendering
**Learning:** Rendering posts on the home page without prefetching related foreign keys (`author`, `category`) and many-to-many fields (`tags`) causes an N+1 query overhead. For 6 posts, database queries balloon from 2 up to 19 queries.
**Action:** Always apply `select_related('author', 'category')` and `prefetch_related('tags')` when querying Post objects that are rendered with author, category, or tag metadata.
