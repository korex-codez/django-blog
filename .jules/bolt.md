# Bolt's Performance Journal

## 2026-11-02 - Middleware Database Throttling for Per-Request User Tracking
**Learning:** In Django applications with custom middlewares that track user presence (e.g. updating `Profile.last_seen`), naive implementations perform a `Profile.objects.get()` (SELECT) followed by `profile.save()` (UPDATE of all fields) on *every* HTTP request made by an authenticated user. This causes significant database write pressure and serialization contention.
**Action:** Throttle the update interval using `django.core.cache.cache` (e.g. 300s TTL) and execute `Profile.objects.filter(user=request.user).update(last_seen=now)` to skip the SELECT query entirely and perform only a fast, targeted UPDATE when the cache key expires.
