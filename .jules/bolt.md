## 2025-05-18 - Throttle Per-Request Middleware Updates with Django Cache
**Learning:** Custom tracking middlewares like `ActiveUserMiddleware` updating `Profile.last_seen` on every HTTP request trigger unnecessary SQL UPDATE queries on every request by authenticated users.
**Action:** Throttle per-request database updates in custom tracking middlewares using `django.core.cache` to set a cache key (e.g., TTL 300s) and perform bulk/direct update query `Profile.objects.filter(user=request.user).update(last_seen=now)` only on cache misses.
