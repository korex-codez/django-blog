# Bolt's Performance Journal

## 2026-09-10 - Global Context Processor Query Caching
**Learning:** Global context processors (like `blog.context_processors.base_context`) run on every single HTTP request rendering a template. Without caching, aggregate SQL queries on categories and tags execute redundantly on every page load.
**Action:** Cache evaluated context processor data with `cache.get_or_set` / `cache.get`/`set` using `list(queryset)` to prevent database hits on cold paths across all application views.
