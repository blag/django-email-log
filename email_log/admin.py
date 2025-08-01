from django.contrib import admin
from django.template.defaultfilters import linebreaksbr
from django.utils.translation import gettext as _

from .models import Attachment, Email, Log


class LogInline(admin.StackedInline):
    model = Log
    readonly_fields = [
        "type",
        "timestamp",
        "esp",
        "event_id",
        "reject_reason",
        "mta_response",
        "tags",
        "user_agent",
        "click_url",
        "raw",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "type",
                    "timestamp",
                    "tags",
                ),
            },
        ),
        (
            _("Details"),
            {
                "fields": (
                    "esp",
                    "event_id",
                    "mta_response",
                    "reject_reason",
                    "user_agent",
                    "click_url",
                    "raw",
                ),
                "classes": ["collapse"],
            },
        ),
    )
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AttachmentInline(admin.StackedInline):
    model = Attachment
    verbose_name = "Attachment"
    verbose_name_plural = "Attachments"
    can_delete = False
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "file",
                    "name",
                    "mimetype",
                )
            },
        ),
    )
    readonly_fields = (
        "file",
        "name",
        "mimetype",
    )
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class EmailAdmin(admin.ModelAdmin):
    list_display = ["recipients", "from_email", "subject", "date_sent", "ok"]
    list_filter = ["date_sent", "ok"]
    readonly_fields = [
        "from_email",
        "recipients",
        "cc_recipients",
        "bcc_recipients",
        "reply_to",
        "extra_headers",
        "subject",
        "body_formatted",
        "html_message",
        "date_sent",
        "ok",
    ]
    inlines = [
        AttachmentInline,
        LogInline,
    ]
    search_fields = [
        "subject",
        "body",
        "recipients",
        "cc_recipients",
        "bcc_recipients",
        "extra_headers",
    ]
    exclude = ["body"]

    def has_delete_permission(self, *args, **kwargs):
        request = args[0]
        user = request.user
        return user.is_superuser

    def has_add_permission(self, *args, **kwargs):
        return False

    def body_formatted(self, obj):
        return linebreaksbr(obj.body)

    body_formatted.short_description = "body"


admin.site.register(Email, EmailAdmin)
