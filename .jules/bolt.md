## 2026-03-31 - Throttle Per-Request Middleware DB Updates with Cache

**Learning:** Custom tracking middleware like `ActiveUserMiddleware` updating `Profile.last_seen` on every HTTP request generates 1 SELECT and 1 UPDATE query per request for every authenticated user. Direct `Profile.objects.get().save()` also triggers full model initialization, image optimization checks, and signals.
**Action:** Use `django.core.cache` with a key like `f'active_user_last_seen_{user.id}'` (5-minute timeout) and direct `Profile.objects.filter(user_id=user.id).update(last_seen=now)` to eliminate thousands of redundant database read/write queries.
