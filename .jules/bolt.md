## 2026-03-31 - Optimize Homepage Queries with select_related & prefetch_related
**Learning:** In Django templates where post cards display author, category, and tags, default QuerySets trigger N+1 SQL queries for each post item. Using `select_related('author', 'category')` for ForeignKeys and `prefetch_related('tags')` for ManyToMany fields reduces query count per home page load from 35 down to 12.
**Action:** Always inspect views rendering lists of models with FK/M2M template attributes and pre-load foreign keys/many-to-many fields using `select_related` and `prefetch_related`.
