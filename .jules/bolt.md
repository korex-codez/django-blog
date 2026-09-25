## 2026-03-31 - Throttle Per-Request Middleware Database Updates

**Learning:** `ActiveUserMiddleware` ran `Profile.objects.get()` and `profile.save()` on every HTTP request from authenticated users, creating high database overhead (~2 SQL queries per request).
**Action:** Throttle tracking middleware database updates using `django.core.cache` with a 300-second window and use `QuerySet.update()` to eliminate unnecessary `SELECT` queries and per-request `UPDATE` queries.
