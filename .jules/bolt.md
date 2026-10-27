## 2026-03-29 - Cache Throttling Per-Request Database Writes in Custom Middleware
**Learning:** Uncached tracking in custom middlewares (such as `ActiveUserMiddleware` updating `Profile.last_seen` on every request) triggers SQL `SELECT` and `UPDATE` queries on every single HTTP request for authenticated users. Throttling updates using `django.core.cache` (5-minute TTL) and passing `update_fields=['last_seen']` eliminates unnecessary DB load on subsequent requests.
**Action:** Always check custom middlewares for uncached DB updates and throttle frequent writes using Django cache.
