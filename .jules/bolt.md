# Bolt's Performance Journal

## 2026-11-11 - Throttling Per-Request Database Writes in User Tracking Middleware
**Learning:** `ActiveUserMiddleware` ran on every incoming request, performing a `Profile.objects.get()` SELECT query and a full `Profile.save()` UPDATE query whenever a user was authenticated. Under production load with multiple requests per page (assets, APIs, page loads), this introduces significant database write contention and ~3.5ms overhead per request.
**Action:** Use `django.core.cache` to throttle updates with a TTL (e.g. 300 seconds / 5 minutes) via a lightweight `user_last_seen_{user.id}` cache key, and use direct `QuerySet.filter(...).update(...)` to bypass full model instantiation, validation, and signal dispatch when an update is actually needed.
