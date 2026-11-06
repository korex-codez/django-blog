# Bolt's Performance Journal

## 2026-11-06 - N+1 Query Cascade on Post Card Rendering in Django Views
**Learning:** In Django templates rendering post card loops (such as `home.html` and `post_list`), template tags access foreign keys (`post.author.username`, `post.category.name`), many-to-many relationships (`post.tags.all`), and model methods (`post.total_likes()`). Calling `post.total_likes()` executes `self.likes.count()` on every card iteration unless `like_count` is annotated and checked in the model method (`if hasattr(self, 'like_count')`).
**Action:** Always combine `.select_related('category', 'author')`, `.prefetch_related('tags')`, and `.annotate(like_count=Count('likes'))` on post list querysets, and support pre-annotated attributes within model count helper methods to prevent O(N) query cascades.
