## 2026-03-01 - ActiveUserMiddleware Database Query Throttling

**Learning:** Running database UPDATE queries on every HTTP request in custom tracking middleware (such as `ActiveUserMiddleware` updating `Profile.last_seen`) creates a major database performance bottleneck for authenticated requests. Using Django's cache layer (`django.core.cache.cache`) to throttle the frequency of database writes (e.g. once every 5 minutes / 300 seconds) eliminates 1 SQL UPDATE query per request while preserving accurate activity timestamp tracking.

**Action:** Whenever implementing per-request user activity tracking or last-seen timestamps in middleware or signals, always wrap DB updates in a cache check with a sensible TTL (e.g., 300 seconds) and pass `update_fields=['last_seen']` to `save()` to optimize DB I/O.
