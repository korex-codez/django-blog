## 2026-03-09 - Django Template N+1 Query Optimization in Post Cards

**Learning:** Accessing `post.author.username`, `post.category.name`, and `post.tags.all` inside template rendering loops for post cards generates N+1 queries for every rendered post if querysets are unoptimized (up to 35 DB queries on the homepage).

**Action:** Always use `.select_related('author', 'category')` for ForeignKeys and `.prefetch_related('tags')` for ManyToMany relationships on Post querysets across all list and card rendering views.
