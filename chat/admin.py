from django.contrib import admin

from .models import *

class ConversationAdmin(admin.ModelAdmin):
    list_display = (
        "initiator", "receiver", "timestamp",
    )
    search_fields = ("initiator", "receiver",)

class MessageAdmin(admin.ModelAdmin):
    list_display = (
         "sender", "receiver",
        )
    search_fields = ("sender", "receiver",)

admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)