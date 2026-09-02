## 2026-09-02 - Eliminate N+1 queries on post list views via ORM eager loading
**Learning:** Django views rendering post lists (`home`, `search_posts`, `category_posts`, `tag_posts`) triggered N+1 queries when accessing `author`, `category`, and `tags` attributes in templates.
**Action:** Always apply `.select_related('author', 'category')` for foreign keys and `.prefetch_related('tags')` for M2M relations on `Post` list QuerySets to batch load related models in fewer queries.
