# Bolt's Journal - Critical Learnings

## 2026-03-30 - Throttling middleware database updates with cache
**Learning:** Per-request database updates in middleware (e.g. updating `Profile.last_seen` on every HTTP request) add unnecessary SQL query overhead (SELECT + UPDATE) on every single request made by an authenticated user.
**Action:** Use `django.core.cache` to key user activity by `request.user.id` with a timeout (e.g., 300 seconds) so database writes are throttled to at most once per cache TTL period, and specify `update_fields=['last_seen']` when saving.
