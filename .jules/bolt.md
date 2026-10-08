## 2026-08-25 - Cache Throttling for Per-Request Active User Updates
**Learning:** Per-request database writes (e.g. updating `Profile.last_seen` in active user tracking middleware) execute SELECT and UPDATE SQL queries on every HTTP request for authenticated users, creating a severe database write bottleneck.
**Action:** Always throttle tracking updates in Django middleware using `django.core.cache` (e.g. 300s TTL cache key) and restrict writes using `update_fields=['last_seen']`.
