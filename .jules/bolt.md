## 2026-09-18 - Eliminate N+1 queries using select_related and prefetch_related
**Learning:** In Django views rendering lists of posts or post details, accessing related fields (such as `post.author`, `post.category`, `post.tags`, or comment `author.profile`) without `select_related` or `prefetch_related` triggers N+1 database queries for every item in the queryset.
**Action:** Always wrap Django Post and Comment querysets with `.select_related('author', 'category')` and `.prefetch_related('tags')` when rendering templates that access these related model attributes.
