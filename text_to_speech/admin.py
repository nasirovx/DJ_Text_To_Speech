from django.contrib import admin
from .models import Text_to_speech


@admin.register(Text_to_speech)
class Text_to_speechAdmin(admin.ModelAdmin):
    list_display = ("text", "file_name", "created_at", "updated_at")
    search_fields = ("text", "file_name")
    list_filter = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        ("Основная информация", {"fields": ("text", "file_name")}),
        (
            "Важные даты",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("file_name",) + self.readonly_fields
        return self.readonly_fields
