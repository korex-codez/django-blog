from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _

class BlogAdminSite(AdminSite):
    site_header = _('MyBlog Administration')
    site_title = _('MyBlog Admin')
    index_title = _('Welcome to MyBlog Admin Panel')
    
    def get_app_list(self, request):
        """Customize app list display"""
        app_list = super().get_app_list(request)
        
        # Custom ordering of apps
        custom_order = {
            'Blog': 1,
            'Authentication and Authorization': 2,
        }
        
        for app in app_list:
            if app['name'] in custom_order:
                app['order'] = custom_order[app['name']]
            else:
                app['order'] = 999
        
        app_list.sort(key=lambda x: x.get('order', 999))
        return app_list

# Create a custom admin site instance
custom_admin_site = BlogAdminSite(name='blog_admin')