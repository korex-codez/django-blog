# Bolt's Journal - Critical Performance Learnings

## 2026-03-31 - Per-request User Activity Tracking Overhead
**Learning:** `ActiveUserMiddleware` executes a database lookup and `save()` on every HTTP request for authenticated users, causing significant SQL SELECT/UPDATE overhead on all views.
**Action:** Throttle tracking in middleware with Django's `cache` (e.g., 300s TTL) and use `save(update_fields=['...'])` to skip DB queries on warm cache requests.
