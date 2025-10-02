from django.contrib import admin
from .models import SuspiciousLink, SuspiciousMessage, UserProfile


@admin.register(SuspiciousLink)
class SuspiciousLinkAdmin(admin.ModelAdmin):
    list_display = ("url", "risk_level", "user", "date_checked")
    list_filter = ("risk_level", "date_checked", "is_suspicious")
    search_fields = ("url", "user__username")
    readonly_fields = ("date_checked",)


@admin.register(SuspiciousMessage)
class SuspiciousMessageAdmin(admin.ModelAdmin):
    list_display = ("get_message_preview", "risk_level", "user", "date_checked")
    list_filter = ("risk_level", "date_checked", "is_suspicious")
    search_fields = ("message", "user__username")
    readonly_fields = ("date_checked",)

    def get_message_preview(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    get_message_preview.short_description = "Message"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "total_checks", "threats_detected", "date_joined")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("date_joined",)