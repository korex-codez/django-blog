## 2025-05-18 - Throttle database updates in per-request tracking middleware
**Learning:** Middleware attached to the request/response processing cycle (such as `ActiveUserMiddleware`) executes on every single HTTP request. Performing unthrottled database writes (like `profile.save()`) in such middleware creates unnecessary database load and slows down response latency for all authenticated requests.
**Action:** Always wrap per-request database updates in middleware with a cache throttle using `django.core.cache`. Use `update_fields` when calling `.save()` to minimize SQL execution overhead.
