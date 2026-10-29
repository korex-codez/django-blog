## 2026-10-29 - Throttle Per-Request Middleware DB Updates
**Learning:** Updating user tracking attributes (like `Profile.last_seen`) directly in custom middleware executes a SQL SELECT and UPDATE on every single HTTP request. This creates heavy database write contention and slows down request processing.
**Action:** Use Django's cache (`django.core.cache.cache`) with a TTL (e.g. 300 seconds) to throttle database updates in tracking middleware.
