# Bolt's Journal - Critical Learnings

## 2026-03-29 - Throttling User Last Seen Database Updates
**Learning:** Middleware executing DB queries (`Profile.objects.get` and `save()`) on every request causes high DB overhead for active users.
**Action:** Use `django.core.cache` to throttle periodic user profile updates (e.g., `last_seen`) with a 5-minute cache TTL.
