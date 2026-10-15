## 2026-08-25 - Throttle Per-Request Middleware DB Updates
**Learning:** Updating `Profile.last_seen` or tracking models in custom Django middlewares on every HTTP request produces 2 SQL queries (`SELECT` + `UPDATE`) per request for authenticated users, generating heavy database CPU load and lock contention. Using `django.core.cache` to throttle updates with a 5-minute (300s) TTL eliminates these SQL queries for ~99% of requests.
**Action:** Always check `cache.get(cache_key)` before executing DB updates in tracking middleware.
