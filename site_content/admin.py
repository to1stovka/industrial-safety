from django.contrib import admin
from .models import Accordion, AccordionItem


class AccordionItemInline(admin.TabularInline):
    model = AccordionItem
    extra = 0
    fields = ("order", "text", "url", "file")
    ordering = ("order",)


@admin.register(Accordion)
class AccordionAdmin(admin.ModelAdmin):
    list_display = ("title", "code")
    search_fields = ("title", "code")
    inlines = [AccordionItemInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("code",)
        return ()