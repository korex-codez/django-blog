## 2026-03-31 - Pre-annotating ManyToMany counts on Django model methods
**Learning:** Calling model methods like `post.total_likes()` inside Django template loops triggers an extra `SELECT COUNT(*)` query for each post card (N+1 queries), even when `.select_related()` and `.prefetch_related()` are used on ForeignKeys and ManyToMany relations.
**Action:** Annotate `.annotate(like_count=Count('likes'))` in post list QuerySets and update model method `total_likes()` to check `if hasattr(self, 'like_count'): return self.like_count`.
