## 2026-03-30 - N+1 Query Fix for Category and Tag API Endpoints
**Learning:** Evaluating related counts in list comprehensions (e.g. `cat.posts.filter(status='published').count()`) triggers an individual SQL `COUNT` query for every item returned by the queryset.
**Action:** Use Django's `.annotate(post_count=Count('posts', filter=Q(posts__status='published')))` to calculate counts in the primary database query, reducing total endpoint query count from O(N) to O(1).
