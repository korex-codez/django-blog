# Bolt's Performance Journal

## 2026-11-02 - Middleware Database Write Bottleneck on Authenticated Requests
**Learning:** `ActiveUserMiddleware` ran a `Profile.objects.get(user=request.user)` followed by `profile.save()` on every single HTTP request by an authenticated user. This generated 2 database queries (SELECT + UPDATE) on every page hit or API request. In a benchmark of 100 requests, this took ~351ms and executed 200 queries.
**Action:** Throttle tracking updates via `django.core.cache` (5-minute TTL) and use direct `QuerySet.update(...)` (`Profile.objects.filter(user=request.user).update(last_seen=...)`) instead of loading and saving the model instance. This reduced 100 benchmark requests to ~3.8ms and eliminated 199 database queries.
