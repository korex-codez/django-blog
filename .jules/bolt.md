# Bolt's Journal

## 2026-03-31 - Throttle Database Updates in Custom Tracking Middleware
**Learning:** Middleware attached to every request (like tracking `Profile.last_seen`) causes an SQL SELECT and UPDATE query on every single HTTP request from authenticated users, resulting in significant DB contention. Using `django.core.cache` to throttle updates with a TTL (e.g., 300 seconds) reduces DB writes by over 99% for active sessions without noticeable loss in accuracy.
**Action:** Always check custom tracking middleware for untrottled DB writes and wrap updates with a cache check.
