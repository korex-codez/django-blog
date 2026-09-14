## 2026-03-31 - N+1 Queries in Django Homepage Post Listing
**Learning:** Accessing `post.author`, `post.category`, `post.tags.all`, and `post.likes.count` (via `total_likes`) during Django template rendering without eager loading triggers N+1 database queries for each post item rendered on the homepage.
**Action:** Always pre-fetch foreign key relations (`select_related('author', 'category')`) and many-to-many associations (`prefetch_related('tags', 'likes')`) on list views rendering post cards.
