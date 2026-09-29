## 2025-05-18 - Throttle DB updates in ActiveUserMiddleware
**Learning:** Updating `Profile.last_seen` directly on every request causes unnecessary database writes for active authenticated users.
**Action:** Use `django.core.cache` to throttle DB updates for `Profile.last_seen` with a 300-second TTL and restrict save fields using `update_fields=['last_seen']`.
