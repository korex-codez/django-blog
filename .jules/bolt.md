## 2026-03-30 - Throttle Middleware Database Updates

**Learning:** Updating database fields on every HTTP request in custom middleware (such as `Profile.last_seen`) creates severe database I/O bottlenecks by performing `SELECT` and `UPDATE` queries on every request.
**Action:** Use `django.core.cache` to set a TTL (e.g. 300 seconds) for user activity tracking and execute `Profile.objects.filter(...).update(...)` only when the cache key has expired.
