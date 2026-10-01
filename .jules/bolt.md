## 2026-10-01 - Throttle Middleware Database Updates

**Learning:** Per-request database updates in middleware (such as updating `Profile.last_seen` on every HTTP request) create excessive SQL write queries that degrade performance under load.
**Action:** Use `django.core.cache` to throttle periodic database updates per user (e.g., 5-minute cache TTL) before executing DB updates in custom tracking middleware.
