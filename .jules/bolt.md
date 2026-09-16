## 2026-08-25 - Django ORM N+1 Query Optimization for Post Listings
**Learning:** In `home.html` and other post list templates, accessing `post.author.username`, `post.category.name`, and `post.tags.all()` inside template loops executes additional SQL queries for every post card if relationships are not pre-fetched.
**Action:** Always chain `.select_related('author', 'category')` and `.prefetch_related('tags')` on `Post` list querysets in views.
