## 2026-08-25 - Throttle Per-Request Profile last_seen Database Updates

**Learning:** Per-request middleware like `ActiveUserMiddleware` that updates `Profile.last_seen` on every HTTP request executes SQL SELECT and UPDATE queries on every single request by authenticated users, creating a major database bottleneck under load. Using `django.core.cache` to throttle updates (e.g. to once every 5 minutes) and using `QuerySet.update()` eliminates unnecessary database queries for subsequent requests.

**Action:** Always wrap per-request database updates in middleware with cache-based throttling using `cache.get()` and `cache.set()`.
