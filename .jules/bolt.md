## 2026-08-25 - Throttle Per-Request Middleware DB Updates
**Learning:** Custom tracking middlewares executing `Profile.objects.get()` and `profile.save()` on every HTTP request create significant database write load (1 SELECT + 1 UPDATE per page view).
**Action:** Use `django.core.cache` to throttle updates to once per 5-minute window per user, and use `update_fields=['last_seen']` during `save()` to update only the affected column.
