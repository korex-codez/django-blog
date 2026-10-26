## 2026-03-31 - Cache-Throttled User Tracking in Middleware

**Learning:** Unthrottled custom tracking middlewares (like updating `Profile.last_seen` on every HTTP request) trigger continuous database `SELECT` and `UPDATE` queries on every request for authenticated users. This creates significant database lock contention and overhead under high traffic.
**Action:** Use `django.core.cache` in middleware to set a cache lock key (e.g., `300` seconds TTL) so database updates for last active/seen timestamps occur at most once per cache window per user. Use `save(update_fields=['last_seen'])` to minimize update SQL scope.
