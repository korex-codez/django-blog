## 2025-05-18 - Throttling Per-Request Database Updates in Tracking Middleware
**Learning:** Updating models (such as `Profile.last_seen`) in custom tracking middleware on every HTTP request creates a massive database bottleneck by firing SQL queries on every page load and API call.
**Action:** Use `django.core.cache` to throttle per-user database updates (e.g. once every 5 minutes) and use `QuerySet.update()` instead of `Model.save()` to avoid unnecessary `SELECT` queries before `UPDATE`.
