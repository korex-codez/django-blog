# Bolt's Performance Journal

## 2026-11-04 - Post card rendering causes N+1 SQL cascades
**Learning:** In Django templates rendering post cards (like `home.html`, `post_list.html`), referencing `post.category`, `post.author`, `post.tags.all`, and `post.total_likes` triggers 4 extra SQL queries per post. On standard paginated listings of 6 posts plus 3 featured posts, this generates between 29 and 36 queries per request.
**Action:** Always eagerly load relationships and precalculate aggregations on `Post` querysets using `.select_related('category', 'author').prefetch_related('tags').annotate(like_count=Count('likes'))`, and guard model helper methods like `total_likes()` to check `if hasattr(self, 'like_count')` first.
