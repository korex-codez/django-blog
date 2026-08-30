## 2026-08-30 - Eager Loading Post Querysets for Home Page & Post ListView

**Learning:** Django views rendering post cards access `author`, `category`, and `tags` attributes on each `Post` instance in template loops, causing N+1 database query overhead (~35 queries per home page render).
**Action:** Always apply `select_related('author', 'category')` for foreign keys and `prefetch_related('tags')` for many-to-many fields when fetching lists of posts for rendering. This reduces the query count to ~12 (~65% query reduction).
