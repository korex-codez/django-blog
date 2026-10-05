# Bolt's Journal - Critical Learnings

## 2026-03-31 - Throttle Per-Request DB Updates in Middleware
**Learning:** Custom tracking middlewares like `ActiveUserMiddleware` that run on every HTTP request can cause significant DB overhead by executing SQL SELECT and UPDATE queries for every request made by authenticated users.
**Action:** Throttle per-request DB updates using `django.core.cache` with a cache key (e.g. 5-minute TTL) and use `QuerySet.update()` to avoid unnecessary `SELECT` calls before `UPDATE`.
