## 2026-10-10 - Cache-throttling per-request middleware database updates
**Learning:** Custom tracking middlewares like `ActiveUserMiddleware` that update timestamps (e.g., `Profile.last_seen`) execute SQL SELECT and UPDATE queries on every HTTP request for authenticated users, creating a major database load bottleneck under active user traffic.
**Action:** Use `django.core.cache` to throttle per-user database updates to fixed intervals (e.g., 300 seconds) and restrict updates with `update_fields=['last_seen']`.
