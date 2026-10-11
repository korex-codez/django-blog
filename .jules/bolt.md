## 2026-08-25 - Throttle Per-Request Database Updates in Tracking Middlewares

**Learning:** Tracking user activity or updating timestamps (such as `Profile.last_seen`) in custom Django middleware without throttling executes SQL `SELECT` + `UPDATE` queries on every HTTP request by authenticated users. This produces unnecessary database load and write lock contention on high-traffic sites.

**Action:** Wrap database updates in custom tracking middlewares using `django.core.cache` to throttle execution (e.g., at most once every 300 seconds per user) and use `QuerySet.update()` to eliminate redundant `SELECT` queries before `UPDATE`.
