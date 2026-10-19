## 2025-05-18 - Per-Request Database Write Throttling in Middleware
**Learning:** Middleware tracking user active state (like updating `Profile.last_seen`) generates an SQL SELECT and UPDATE query on every single HTTP request from authenticated users, scaling directly with request throughput and overloading the database.
**Action:** Always throttle per-request database writes in custom tracking middlewares using `django.core.cache` (e.g. 300s TTL cache keys) and direct `filter().update()` queries.
