from django.contrib import admin

from django_website.logger.models import Message, Channel


class MessageAdmin(admin.ModelAdmin):
    list_display = ("text", "nickname", "channel", "logged")
    list_filter = ("channel", "logged")
    search_fields = ["text"]


class ChannelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Message, MessageAdmin)
admin.site.register(Channel, ChannelAdmin)
