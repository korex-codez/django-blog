## 2026-03-31 - Cache throttling for per-request user activity tracking
**Learning:** `ActiveUserMiddleware` was executing a database `UPDATE` query on `Profile.last_seen` on every single HTTP request from authenticated users. Using `django.core.cache` to throttle updates to a 5-minute window eliminates ~99% of these write queries during active sessions.
**Action:** Always check custom tracking middleware for per-request database writes and wrap them with `django.core.cache` TTL keys.
