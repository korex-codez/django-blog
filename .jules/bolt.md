## 2026-09-19 - Django Template Default Filter Triggers N+1 Queries on Zero Count

**Learning:** When using Django ORM annotations (e.g., `like_count=Count('likes')`), template expressions like `{{ post.like_count|default:post.total_likes }}` treat an integer count of `0` as falsy. This causes the `default` filter to evaluate `post.total_likes()`, triggering an extra SQL `COUNT` query for every item with 0 likes and re-introducing the N+1 query problem.

**Action:** Use explicit conditional checks (`{% if post.like_count is not None %}{{ post.like_count }}{% else %}{{ post.total_likes }}{% endif %}`) when falling back from annotated counts to model methods, ensuring 0 is treated as a valid count.
