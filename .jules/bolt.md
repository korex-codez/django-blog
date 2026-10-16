# Bolt's Journal - Critical Learnings

## 2025-05-10 - ActiveUserMiddleware Database Query Throttling
**Learning:** Custom tracking middlewares like `ActiveUserMiddleware` updating `Profile.last_seen` on every authenticated request execute SQL `UPDATE` queries on every single HTTP response, severely degrading response times. Throttling updates using `django.core.cache` prevents database writes on every request while maintaining accurate last-seen timestamps.
**Action:** Always check custom tracking middlewares for per-request database writes and wrap DB updates in a cache key timeout check.
