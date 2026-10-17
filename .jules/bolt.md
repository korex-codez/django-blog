## 2025-10-18 - Middleware Database Query Throttling
**Learning:** Custom tracking middleware like `ActiveUserMiddleware` executing `Profile.objects.get` and `profile.save()` on every request adds 2 database queries (`SELECT` + `UPDATE`) per HTTP request for authenticated users. Throttling updates using `django.core.cache` (5 min TTL) and `update_fields=['last_seen']` reduces database queries on cached requests to zero.
**Action:** Always check custom middlewares in Django apps for per-request database operations and throttle them with `django.core.cache`.
