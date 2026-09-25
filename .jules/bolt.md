# Bolt's Journal - Critical Learnings

## 2026-09-25 - Post Queryset Preloading with select_related and prefetch_related
**Learning:** Rendering post cards across home, post list, search, category, and tag pages triggers N+1 database queries for post authors, categories, and tags if querysets are unoptimized.
**Action:** Always chain `.select_related('category', 'author').prefetch_related('tags')` on `Post` list querysets in Django views before passing them to card templates.
