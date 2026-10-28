## 2026-03-31 - Throttle Per-Request Middleware Database Writes with Cache
**Learning:** Per-request tracking middlewares like `ActiveUserMiddleware` execute `SELECT` and `UPDATE` queries on every HTTP request for authenticated users, creating a major database query bottleneck and increasing response latency.
**Action:** Always throttle middleware database updates using `django.core.cache` (e.g., 300s TTL cache key) and restrict update queries to `update_fields=['last_seen']`.
