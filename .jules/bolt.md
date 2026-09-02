## 2026-03-31 - Django ORM N+1 Query Prevention on Post List Cards
**Learning:** Post listing pages (`home`, `PostListView`, `search_posts`, `category_posts`, `tag_posts`) render post cards accessing `post.author`, `post.category`, and `post.tags`. Without eager loading, rendering 6+ posts triggers separate SQL queries for each related model (N+1 bottleneck).
**Action:** Always chain `.select_related('author', 'category').prefetch_related('tags')` on Post querysets when rendering post list cards to reduce database queries from 28+ down to 5.
