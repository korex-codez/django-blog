## 2026-09-17 - Django Query Optimization & Context Processor Caching

**Learning:** Rendering post cards on home and list views triggered N+1 query cascades (fetching author, category, tags, and likes individually for each post rendered). Additionally, uncached global context processors running aggregate `Count` queries on every request added unnecessary DB overhead across all pages.
- Query count on home page before optimization: 35 queries.
- Query count after adding `select_related('author', 'category')`, `prefetch_related('tags', 'likes')`, and caching `base_context`: 7 queries (~80% reduction).

**Action:** Always inspect views rendering model lists for missing `select_related`/`prefetch_related`. Ensure global context processors cache expensive ORM aggregate queries.
