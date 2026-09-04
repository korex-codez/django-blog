## 2026-09-04 - Django QuerySet Optimization & Template Method Overhead

**Learning:** Calling model instance methods in templates (such as `{{ post.total_likes }}`) when rendering lists triggers N+1 SQL queries if the method performs a relation count query. Using QuerySet `.annotate(like_count=Count('likes'))` alongside `select_related` and `prefetch_related`, and checking `hasattr(self, 'like_count')` within the model method transparently reuses prefetched query data.

**Action:** Whenever optimizing Django list views, inspect model methods called inside template loops for relation queries, and combine `.annotate()` with `hasattr()` checks on the model method to avoid template N+1 query loops.
