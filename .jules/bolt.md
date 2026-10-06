## 2026-08-25 - Throttle active user tracking in middleware using cache

**Learning:** Per-request middleware updates to model fields (e.g., `Profile.last_seen`) execute SQL `SELECT` and `UPDATE` queries on every HTTP request by authenticated users. Throttling database updates with `django.core.cache` (5 min window) and using direct `QuerySet.update()` on cache misses eliminates DB load for 99%+ of requests while preserving user activity tracking.
**Action:** Always check custom tracking middlewares for per-request database writes and throttle them using cache.
