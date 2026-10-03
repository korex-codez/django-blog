# Bolt's Journal - Critical Learnings

## 2026-03-30 - Database update throttling in Django Middlewares
**Learning:** Custom tracking middleware like `ActiveUserMiddleware` executing `Profile.objects.get` and `profile.save()` on every HTTP request creates a significant database bottleneck by running 2 extra SQL queries (1 SELECT, 1 UPDATE) per request for authenticated users.
**Action:** Use `django.core.cache` to set a cache key with a expiration timeout (e.g. 300 seconds) when updating user stats or last seen timestamps to throttle database writes.
