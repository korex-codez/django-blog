## 2025-05-18 - Per-request Middleware Database Updates
**Learning:** Per-request tracking middleware such as `ActiveUserMiddleware` updating `Profile.last_seen` executes 1 `SELECT` and 1 `UPDATE` database query on every HTTP request by authenticated users. Throttling updates using Django's cache framework eliminates redundant database queries.
**Action:** Always check custom middlewares for synchronous DB writes on every request and use `cache.get()` / `cache.set()` with a throttling window (e.g., 300s) and `update_fields` when saving.
