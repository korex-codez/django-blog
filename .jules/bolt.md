## 2026-10-15 - Throttle Per-Request Middleware Database Updates

**Learning:** Per-request custom tracking middleware like `ActiveUserMiddleware` updating `Profile.last_seen` executes `SELECT` and `UPDATE` SQL queries on every single HTTP request for authenticated users. This leads to write amplification and database lock contention under load.
**Action:** Use `django.core.cache` to throttle per-request user activity/timestamp updates (e.g. setting a cache flag for 300 seconds) to avoid database writes on every request while maintaining accurate activity tracking.
