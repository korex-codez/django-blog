## 2026-09-28 - Throttle Middleware Database Queries with Django Cache
**Learning:** Custom tracking middlewares like `ActiveUserMiddleware` that run on every HTTP request can execute unthrottled `SELECT` and `UPDATE` queries on every page hit for authenticated users, creating a serious database bottleneck.
**Action:** Always throttle per-request database updates in middleware using `django.core.cache` with an appropriate TTL (e.g., 300 seconds) to avoid redundant SQL queries on active user sessions.
