# Bolt's Performance Journal

## 2026-10-31 - Throttle Per-Request Middleware Database Writes
**Learning:** `ActiveUserMiddleware` ran `Profile.objects.get()` followed by `profile.save()` on every HTTP request by authenticated users. This added 2 blocking database queries (one SELECT, one full UPDATE) to every request cycle, causing severe DB load.
**Action:** Throttle presence and activity tracking in custom middlewares using `django.core.cache` (e.g. 5-minute cache key per user) and execute a direct `QuerySet.filter(...).update(...)` instead of an instance `.save()`. This drops per-request queries from 2 to 0 on cache hits and eliminates the unnecessary SELECT on cache misses.
