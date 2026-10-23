# Bolt's Journal - Critical Learnings

## 2026-03-29 - Cache-Throttled User Tracking Middleware
**Learning:** Un-throttled tracking middlewares that update database models (e.g. `Profile.last_seen`) execute `SELECT` and `UPDATE` queries on every HTTP request for authenticated users. This adds 2 database queries per request and creates DB contention under concurrency.
**Action:** Always throttle per-request database updates in custom tracking middlewares using `django.core.cache`. Use direct `queryset.update()` to avoid `SELECT` queries and store a cache key with TTL (e.g. 300 seconds) so DB writes only occur once per interval per user session.
