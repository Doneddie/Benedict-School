from django.contrib import admin
from .models import Event, About, GalleryImage

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