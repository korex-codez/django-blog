# Bolt's Performance Journal

## 2026-11-01 - ActiveUserMiddleware per-request database thrashing
**Learning:** `ActiveUserMiddleware` ran a SELECT query (`Profile.objects.get`) followed by a full-table UPDATE query (`profile.save()`) on every request made by an authenticated user. In high-traffic apps, executing write queries on every single request creates database contention and severe latency bottlenecks.
**Action:** Throttle presence tracking using Django's cache layer (`cache.get`/`cache.set` with a 5-minute TTL) and use direct queryset update (`Profile.objects.filter(user=request.user).update(last_seen=now)`) to eliminate the SELECT query on cache misses and eliminate all queries on cached hits.
