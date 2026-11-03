# Bolt's Performance Journal

## 2026-11-03 - Throttling middleware per-request database updates
**Learning:** `ActiveUserMiddleware` ran a SELECT and full-table-column UPDATE on `Profile` on every single request made by authenticated users, causing write lock contention and 2 extra database queries per request. Using `django.core.cache` to throttle updates (5-minute TTL) along with direct `QuerySet.filter(...).update(...)` eliminates redundant DB writes and saves 2 queries on subsequent requests.
**Action:** Always check tracking middlewares for unthrottled database writes and optimize them using cache and direct queryset updates.
