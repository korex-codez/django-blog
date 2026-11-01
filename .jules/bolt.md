# Bolt's Journal

## 2026-08-25 - Throttle per-request database updates in tracking middleware
**Learning:** Middleware tracking user actions (like `ActiveUserMiddleware` updating `Profile.last_seen`) executed `Profile.objects.get` followed by `profile.save()` on every request made by authenticated users. This added 2 synchronous database queries per request, creating latency and database write bottlenecks.
**Action:** Throttle tracking updates using `django.core.cache.cache` (e.g. 300 seconds TTL) and replace `get()` + `save()` with direct `QuerySet.filter(...).update(...)` to execute at most 1 query per interval and zero queries during cache hits.
