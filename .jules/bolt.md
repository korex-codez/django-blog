## 2026-03-31 - Eager loading Django relations to eliminate N+1 queries
**Learning:** Rendering Django templates containing lists of model instances that reference ForeignKeys (such as `post.author`, `post.category`, and `post.author.profile`) and ManyToMany fields (`post.tags`) generates an N+1 query overhead for each rendered post if relations aren't pre-fetched.
**Action:** Always wrap Django ORM queries for list views and cards with `.select_related('author', 'category', 'author__profile')` and `.prefetch_related('tags')` to reduce query count on post list rendering by ~90%.
