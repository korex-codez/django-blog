## 2026-10-28 - Cache-throttling per-request database updates in custom middlewares

**Learning:** Custom tracking middlewares (e.g. updating `Profile.last_seen` on every HTTP request for authenticated users) create a massive database bottleneck by executing SELECT and UPDATE queries on every single HTTP request. By leveraging Django's `cache` module to set a 5-minute TTL throttling key, per-request DB write overhead is eliminated for ~99% of requests while maintaining last_seen accuracy.

**Action:** Always check custom middlewares for synchronous DB reads/writes on every HTTP request and wrap them in Django cache key checks with reasonable TTLs.
