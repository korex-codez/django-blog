## 2026-03-31 - [Throttling tracking middleware DB updates]
**Learning:** Custom tracking middleware like `ActiveUserMiddleware` executing `Profile.objects.get()` and `profile.save()` on every HTTP request creates severe database overhead (1 SELECT + 1 UPDATE per request).
**Action:** Throttle tracking updates using `django.core.cache` to set a cache key per user (e.g. 300s expiration) and perform updates via direct `QuerySet.update()` only when the cache key is missing.
