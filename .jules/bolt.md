## 2026-03-29 - Throttle per-request middleware database updates
**Learning:** Updating models (such as `Profile.last_seen`) inside middleware on every HTTP request produces unnecessary SQL queries per request for authenticated users. Throttling updates using `django.core.cache` (5 min TTL) and applying single-query `Profile.objects.filter(...).update(...)` eliminates per-request database overhead.
**Action:** Always check middleware and request lifecycle hooks for per-request database writes, and wrap them with cache throttling.
