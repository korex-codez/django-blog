## 2025-05-18 - Throttle ActiveUserMiddleware DB Updates with Django Cache
**Learning:** `ActiveUserMiddleware` ran a SELECT and UPDATE query on `Profile.last_seen` for every HTTP request from an authenticated user, creating significant database overhead.
**Action:** Use `django.core.cache` with a 300-second TTL to throttle per-request tracking and use `Profile.objects.filter(...).update(...)` to avoid unnecessary SELECT queries before UPDATE.
