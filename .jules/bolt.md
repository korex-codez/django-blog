# Bolt's Journal - Critical Learnings

## 2026-10-30 - Cache-throttling per-request database updates in tracking middleware
**Learning:** Middleware tracking user presence (`ActiveUserMiddleware`) by updating `Profile.last_seen` on every single HTTP request causes massive database write amplification and lock contention. Even on read-only endpoints, each authenticated request triggered an SQL UPDATE query.
**Action:** Throttle presence tracking via `django.core.cache.cache` with a cache key like `last_seen_user_{user_id}` and a 5-minute timeout. Check the cache before executing database updates, reducing per-request writes by ~99% for active browsing sessions.
