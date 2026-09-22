## 2026-03-31 - Optimize Django Post querysets with select_related and prefetch_related
**Learning:** Post list views on the home page suffered from an N+1 query pattern when fetching post author, category, and tags in Django templates. Adding `.select_related('author', 'category')` and `.prefetch_related('tags')` reduced the database query count from 43 to 2 queries per request.
**Action:** Always check `Post.objects` querysets rendered in templates with relations for missing `select_related` / `prefetch_related` calls.
