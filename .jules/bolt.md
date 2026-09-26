## 2026-08-25 - Throttling User Tracking Middlewares
**Learning:** Custom tracking middlewares like `ActiveUserMiddleware` updating `Profile.last_seen` on every HTTP request create a significant SQL SELECT and UPDATE write amplification on hot request paths. Throttling updates using `django.core.cache` (5 min timeout) and restricting `save()` to `update_fields=['last_seen']` eliminates DB write overhead per request.
**Action:** When tracking per-request user activity in Django middlewares, always throttle database writes using cache and pass explicit `update_fields` to `save()`.
