## 2026-03-31 - Throttling Per-Request Database Updates in Middleware
**Learning:** `ActiveUserMiddleware` ran unthrottled `SELECT` and `UPDATE` queries on `Profile` for every HTTP request made by authenticated users. Using `django.core.cache` to throttle updates with a TTL (e.g., 300 seconds) and combining it with direct `filter().update()` reduces DB query volume by over 99% for active user sessions.
**Action:** Check middleware classes for unthrottled per-request DB writes and apply cache throttling with direct `.update()` calls.
