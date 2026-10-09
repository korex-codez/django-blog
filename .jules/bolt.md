## 2025-05-18 - Throttle ActiveUserMiddleware Database Updates
**Learning:** `ActiveUserMiddleware` runs on every HTTP request and previously updated `Profile.last_seen` synchronously in the database for every authenticated request, adding unnecessary SQL `SELECT` and `UPDATE` latency.
**Action:** Throttle tracking middleware DB writes using `django.core.cache` (e.g. 300s TTL) and use `save(update_fields=['last_seen'])` to minimize write load.
