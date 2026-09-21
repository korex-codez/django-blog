## 2026-09-21 - Eliminate N+1 Database Queries in Home View
**Learning:** In Django templates displaying post cards (`blog/home.html`), accessing `post.author`, `post.category`, `post.tags.all`, and `post.likes.count()` lazily triggers 4 extra SQL queries per post.
**Action:** Always apply `.select_related('author', 'category')` and `.prefetch_related('tags', 'likes')` on `Post` list querysets to keep home page rendering query counts minimal (~7 total queries) regardless of the number of posts on the page.
