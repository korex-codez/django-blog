## 2026-09-16 - Eliminate N+1 Database Queries in Django Views using Annotations and Select/Prefetch Related

**Learning:** In Django API views or page templates iterating over related objects (such as categories/tags with post counts or posts with authors and categories), executing queries inside list comprehensions or template loops causes N+1 SQL queries. Using `Category.objects.annotate(post_count=Count('posts', filter=Q(posts__status='published')))` calculates the count in a single SQL query instead of N separate `filter().count()` calls. Similarly, using `select_related('author', 'category')` on post querysets eliminates separate database queries when accessing foreign key fields during template rendering or JSON serialization.

**Action:** Whenever iterating over querysets that access foreign key attributes or aggregate relationships, use `select_related` / `prefetch_related` or ORM annotations (`annotate`) to retrieve all necessary data in a single SQL query.
