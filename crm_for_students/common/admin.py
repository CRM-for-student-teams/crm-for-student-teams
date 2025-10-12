"""
Reusable admin classes and mixins for the CRM application.
"""
from unfold.admin import ModelAdmin


class BaseModelAdmin(ModelAdmin):
    """
    Base admin class that extends Unfold's ModelAdmin.
    Use this as the base class for all admin classes in the project
    to maintain consistency and easily add shared functionality.
    
    Example usage in other apps:
        from common.admin import BaseModelAdmin
        
        @admin.register(MyModel)
        class MyModelAdmin(BaseModelAdmin):
            list_display = ['name', 'created_at']
    """
    pass
