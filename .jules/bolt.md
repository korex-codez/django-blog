## 2026-03-31 - Django ORM N+1 Query Optimization in Post Querysets
**Learning:** Post cards rendered across `home`, `search_posts`, `category_posts`, `tag_posts`, and `profile_view` templates access related `author`, `category`, and `tags` attributes. Fetching posts without `select_related('author', 'category')` and `prefetch_related('tags')` results in N+1 SQL queries per card.
**Action:** Always chain `select_related('author', 'category')` and `prefetch_related('tags')` onto `Post` querysets when rendering post lists/cards in views.
