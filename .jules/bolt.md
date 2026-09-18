# Bolt's Journal - Critical Learnings & Insights

## 2026-03-30 - N+1 Query Prevention in Post & Comment Trees
**Learning:** Rendering Django blog post listings and comment trees in templates (`post.author.profile.avatar`, `post.tags.all`, `comment.replies`) triggers N+1 database queries if `select_related` and `prefetch_related` are not explicitly defined in the view querysets.
**Action:** Always chain `.select_related('category', 'author', 'author__profile')` and `.prefetch_related('tags')` on Post querysets, and `.select_related('author', 'author__profile')` with `.prefetch_related('replies', 'replies__author', 'replies__author__profile')` on Comment querysets before passing them to Django templates.
