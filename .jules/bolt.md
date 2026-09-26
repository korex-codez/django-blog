## 2026-03-30 - Throttle Profile.last_seen DB updates in ActiveUserMiddleware

**Learning:** `ActiveUserMiddleware` ran a SELECT (`Profile.objects.get`) and UPDATE (`profile.save()`) query on every single HTTP request made by an authenticated user.
**Action:** Throttle `Profile.last_seen` database updates using `django.core.cache` to execute at most once every 300 seconds per user, eliminating 2 database queries per request for logged-in users.
