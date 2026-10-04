## 2026-10-04 - Throttle Per-Request Middleware Database Updates

**Learning:** Un-cached user tracking middlewares that update model fields (like `Profile.last_seen`) on every HTTP request cause redundant `SELECT` and `UPDATE` SQL queries on every single page load or API request made by authenticated users.
**Action:** Use `django.core.cache` with a short TTL (e.g., 5 minutes) to throttle database updates in user activity / tracking middleware, eliminating 2 SQL queries per authenticated request.
