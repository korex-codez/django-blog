## 2026-11-10 - Throttling User Activity Database Updates in Middleware
**Learning:** In Django middleware executed on every request (such as `ActiveUserMiddleware`), updating `last_seen` timestamps via `Profile.objects.get()` and `profile.save()` produces a SELECT and full-table-row UPDATE query on every request made by authenticated users, causing significant database write bottlenecks.
**Action:** Use `django.core.cache` to throttle updates with a TTL (e.g. 5 minutes) and issue a targeted `QuerySet.filter(...).update(...)` to bypass unnecessary SELECT queries and model lifecycle overhead.
