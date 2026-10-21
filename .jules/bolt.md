## 2026-10-21 - Throttle per-request database updates in ActiveUserMiddleware
**Learning:** Custom tracking middlewares like `ActiveUserMiddleware` updating `Profile.last_seen` execute SQL SELECT and UPDATE queries on every HTTP request for authenticated users, creating severe database write overhead.
**Action:** Use `django.core.cache` to throttle `last_seen` database updates to a 5-minute interval and use `Profile.objects.filter(user=request.user).update(last_seen=now)` to eliminate per-request queries.
