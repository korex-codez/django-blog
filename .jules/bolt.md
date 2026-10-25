## 2026-03-31 - ActiveUserMiddleware Database Query Throttling
**Learning:** Per-request database updates in middleware (such as updating `Profile.last_seen` on every request for authenticated users) trigger SQL SELECT and UPDATE queries on every HTTP request, adding database load across all endpoints.
**Action:** Use `django.core.cache` to throttle per-user timestamp updates to a 5-minute interval using `Profile.objects.filter(user=request.user).update(last_seen=timezone.now())` to avoid unnecessary database queries.
