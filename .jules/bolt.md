## 2026-03-31 - Throttle per-request DB updates in custom tracking middleware

**Learning:** Custom tracking middleware (such as `ActiveUserMiddleware`) that executes `Profile.objects.get()` and `profile.save()` on every authenticated request introduces redundant SQL SELECT and SQL UPDATE statements. This creates severe database write amplification and lock contention. Using `django.core.cache` to throttle updates (e.g., caching `user_last_seen_{user.id}` for 300 seconds) reduces DB writes by ~99% for active user sessions.
**Action:** Always check custom Django middlewares for per-request database writes. Wrap timestamp/activity updates with `cache.get`/`cache.set` and use `update_fields` on `save()`.
