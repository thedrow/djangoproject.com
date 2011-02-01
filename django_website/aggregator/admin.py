from __future__ import absolute_import

from django.contrib import admin
from .models import Feed, FeedItem, FeedType, ClaimRequest

admin.site.register(Feed, 
    list_display  = ["title", "feed_type", "public_url"],
    list_filter   = ["feed_type", "is_defunct"],
    ordering      = ["title"],
    search_fields = ["title", "public_url"],
    raw_id_fields = ['owner'],
    list_per_page = 500,
)

admin.site.register(FeedItem, 
    list_display   = ['title', 'feed', 'date_modified'],
    list_filter    = ['feed'],
    search_fields  = ['feed__title', 'feed__public_url', 'title'],
    date_heirarchy = ['date_modified'],
)

admin.site.register(FeedType,
    prepopulated_fields = {'slug': ('name',)},
)

class ClaimRequestAdmin(admin.ModelAdmin):
    list_display = ['__repr__', 'claimant']
    list_filter = ['status']
    actions = ['approve_requests', 'deny_requests']

    def approve_requests(self, request, selected):
        for cr in selected:
            cr.approve()

    def deny_requests(self, request, selected):
        for cr in selected:
            cr.deny()

admin.site.register(ClaimRequest, ClaimRequestAdmin)
