## 2026-03-30 - Throttle Per-Request DB Updates in Custom Middlewares

**Learning:** `ActiveUserMiddleware` was executing a database lookup (`Profile.objects.get`) and `save()` query on every single HTTP request for authenticated users to update `last_seen`. This introduced unnecessary database write contention and response latency. Using `django.core.cache` to throttle updates to once every 300 seconds (5 minutes) per user eliminates >99% of SQL queries executed during active user browsing sessions while preserving timestamp accuracy.

**Action:** Always check `cache.get(cache_key)` and set a cache flag before executing SQL `UPDATE` operations inside per-request middleware hooks. Use `update_fields` when saving models in middleware to restrict query overhead to only necessary columns.
