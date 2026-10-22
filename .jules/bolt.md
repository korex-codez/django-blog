## 2026-03-30 - Throttle Middleware Database Updates with Cache

**Learning:** Un-throttled database writes (such as updating `Profile.last_seen` on every HTTP request in custom tracking middleware) introduce unnecessary DB lock contention and high I/O overhead on every HTTP request for authenticated users.
**Action:** Use `django.core.cache` to throttle per-request user activity/last-seen tracking to execute at most once per cache timeout interval (e.g. 300 seconds), eliminating 99%+ of redundant SQL UPDATE queries for active user sessions.
