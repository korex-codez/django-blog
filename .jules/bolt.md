## 2026-09-23 - Database Query Optimization via select_related and prefetch_related
**Learning:** Post list views (home, search, category, tag) rendered related foreign keys (`category`, `author`) and many-to-many relationships (`tags`) for each post card, causing N+1 query cascades (e.g., ~35 queries on home page).
**Action:** Always chain `.select_related('category', 'author')` and `.prefetch_related('tags')` on Post querysets in list views to reduce queries by over 60%.
