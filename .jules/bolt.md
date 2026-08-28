## 2025-03-04 - Model method fallback for queryset annotations in Django
**Learning:** Model methods like `total_likes()` that call `self.likes.count()` trigger an additional SQL query per instance rendered in a template loop unless checked against an annotated field (e.g. `hasattr(self, 'like_count')`).
**Action:** When adding `.annotate()` on querysets for list views, ensure corresponding model methods inspect `hasattr(self, 'annotated_field')` before executing relational count queries.
