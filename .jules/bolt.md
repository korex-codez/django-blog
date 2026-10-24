## 2026-03-31 - Throttle per-request database updates in middleware
**Learning:** Custom tracking middlewares like `ActiveUserMiddleware` updating model fields (e.g. `Profile.last_seen`) execute SQL SELECT and UPDATE queries on every HTTP request for authenticated users, causing significant database overhead and locking.
**Action:** Use `django.core.cache` to throttle update operations to a specified interval (e.g., 5 minutes) and use `profile.save(update_fields=['last_seen'])` to skip unnecessary signal triggers or image optimizations.
