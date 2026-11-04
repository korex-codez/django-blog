# Bolt's Journal - Critical Learnings

## 2026-03-31 - N+1 Query Elimination in Django Post Lists
**Learning:** In Django list views rendering post cards (like `home` and `post_list`), template tags accessing `post.author`, `post.category`, `post.tags.all`, and `post.total_likes` trigger multiple SQL queries per item (N+1 cascade: 1 for author, 1 for category, 1 for tags, and 1 count query for likes). Modifying `Post.total_likes()` to check `if hasattr(self, 'like_count'): return self.like_count` allows querysets to annotate `like_count=Count('likes')` without breaking existing callers.
**Action:** Chain `.select_related('category', 'author')`, `.prefetch_related('tags')`, and `.annotate(like_count=Count('likes'))` on post querysets in list views, and let `total_likes()` consume the annotation if present.
