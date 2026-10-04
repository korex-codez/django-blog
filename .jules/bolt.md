## 2025-05-18 - Throttling User Tracking Middleware DB Updates
**Learning:** Per-request tracking middleware like `ActiveUserMiddleware` executing `Profile.objects.get()` and `profile.save()` on every request introduces significant SQL overhead (SELECT + UPDATE queries) on all authenticated endpoints.
**Action:** Always throttle non-critical user state updates in middleware using `django.core.cache` key TTLs (e.g., 300 seconds) to bypass redundant database writes.
