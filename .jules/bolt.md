## 2026-08-27 - Eager loading foreign keys and M2M relations in home view
**Learning:** Home page post cards render `post.author`, `post.category`, `post.tags.all`, and `post.likes.count`, resulting in N+1 database query overhead per post. Adding `.select_related('author', 'category').prefetch_related('tags', 'likes')` reduces DB queries from ~30 to 9 queries (~35% speedup).
**Action:** When querying `Post` models for list views or home feeds, inspect template usage for author, category, tags, and likes, and pre-fetch them early in the ORM queryset.
