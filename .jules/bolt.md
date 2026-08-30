## 2026-08-30 - Prevent N+1 queries in Django Post views with select_related & prefetch_related
**Learning:** Rendering list of posts with FK (`author`, `category`) and M2M (`tags`) relationships without `select_related`/`prefetch_related` causes N+1 SQL queries for every post item in templates.
**Action:** Always inspect ORM query counts in Django views rendering model lists with foreign keys/many-to-many fields, and apply `select_related` and `prefetch_related`.
