## 2025-05-18 - Throttle middleware DB updates using cache

**Learning:** `ActiveUserMiddleware` ran `Profile.objects.get` and `profile.save()` on every single HTTP request for authenticated users, executing 2 unnecessary SQL queries per request.
**Action:** Throttle tracking updates using `django.core.cache.cache` with a 300-second TTL and `update_fields=['last_seen']` to eliminate redundant DB activity across requests.
