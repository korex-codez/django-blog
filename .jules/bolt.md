## 2026-03-31 - Throttle Middleware Database Updates with Cache
**Learning:** Custom activity-tracking middleware that executes a DB SELECT and UPDATE query on every single HTTP request creates severe database bottleneck as traffic grows. Throttling updates using Django's cache framework reduces database writes by >99% while keeping user activity tracking accurate enough for real-world usage.
**Action:** Always wrap per-request database updates in custom middlewares (e.g. `last_seen` tracking) with `cache.get()`/`cache.set()` throttling.
