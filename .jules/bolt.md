## 2025-05-18 - Throttle Middleware Database Updates with Cache

**Learning:** Per-request database writes in custom tracking middleware (like `ActiveUserMiddleware` updating `Profile.last_seen`) execute SQL SELECT and UPDATE queries on every HTTP request by authenticated users. Using `django.core.cache` to throttle updates (e.g. key `active_user_last_seen_{user.id}` with a 5-minute TTL) eliminates thousands of redundant DB queries without sacrificing user tracking accuracy. Furthermore, passing `update_fields=['last_seen']` to `profile.save()` prevents full row writes.

**Action:** Always check custom middleware for un-throttled database read/write loops on every HTTP request and wrap them in a cache throttle check with `update_fields` when persisting to DB.
