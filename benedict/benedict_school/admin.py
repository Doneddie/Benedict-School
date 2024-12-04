from django.contrib import admin
from .models import Event, About, GalleryImage, Child

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'description', 'image', 'video')
    list_filter = ('date', 'location')  # filter events by date or location
    search_fields = ('title', 'location', 'description')  # search capability

    # To display image and video in the admin detail page
    fieldsets = (
        (None, {
            'fields': ('title', 'date', 'location', 'description', 'image', 'video')
        }),
    )

admin.site.register(About)

admin.site.register(GalleryImage)

class ChildAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_of_birth', 'study_class', 'application_status']  # List fields to display in the admin list view
    list_filter = ['study_class', 'application_status']  # Add filters to the sidebar

    # Only show 'application_status' field to admins
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:  # Check if the user is not an admin
            fields = [field for field in fields if field != 'application_status']  # Remove application_status for non-admins
        return fields
    
    # Make application_status a read-only field for non-admins
    def has_change_permission(self, request, obj=None):
        # Allow admins to change the status, others can only view it
        if obj and not request.user.is_superuser:
            return False  # Non-admin users can't change the object
        return super().has_change_permission(request, obj)
