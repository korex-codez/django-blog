## 2026-03-31 - Throttle Per-Request Middleware DB Updates
**Learning:** Updating user activity timestamps (e.g. `Profile.last_seen`) in custom tracking middleware on every HTTP request causes high database write contention and unnecessary SELECT + UPDATE overhead.
**Action:** Use `django.core.cache` to throttle activity updates to once per cache window (e.g., 300 seconds) and replace `get()` + `save()` with direct `filter().update()` calls to eliminate extra SELECT queries.
