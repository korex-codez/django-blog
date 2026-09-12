## 2026-03-30 - N+1 Query Optimization for Django Post Cards
**Learning:** Calling `post.total_likes` (which executes `self.likes.count()`) and accessing foreign key attributes (`post.author.username`, `post.category.name`, `post.tags.all()`) inside loops in Django templates causes severe N+1 SQL queries (27+ queries on homepage).
**Action:** Use `.select_related('author', 'category')`, `.prefetch_related('tags')`, and `.annotate(likes_count=Count('likes', distinct=True))` in views, and update model methods to check `hasattr(self, 'likes_count')` before querying the database.
