## 2026-03-30 - Throttle Per-Request Database Updates in Middleware
**Learning:** Custom tracking middlewares (e.g. `ActiveUserMiddleware` updating `Profile.last_seen`) execute SQL `SELECT` + `UPDATE` queries on every HTTP request for authenticated users, causing severe database I/O bottlenecks under concurrent load.
**Action:** Throttle database updates in per-request middleware using `django.core.cache` with a cache key (e.g., 300s TTL) and use `profile.save(update_fields=['last_seen'])` when database updates occur.
