from django.contrib import admin
from landing.models import (CourseDirection,
                            Review,
                            Chunk, 
                            Expert, 
                            MinstroyProgram,
                            Qualification,
                            UnifiedRequest,
                            )
from django.utils.html import format_html

@admin.register(CourseDirection)
class CourseDirectionAdmin(admin.ModelAdmin):
    list_display = ("title", "start_date", "end_date", "mode", "price", "rating", "featured")
    list_filter = ("mode", "featured", "start_date")
    search_fields = ("title",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("category", "rating", "short_text")
    list_filter = ("category", "rating")
    search_fields = ("text",)

    def short_text(self, obj):
        return (obj.text[:80] + "...") if len(obj.text) > 80 else obj.text

    short_text.short_description = "Текст отзыва"


@admin.register(Chunk)
class ChunkAdmin(admin.ModelAdmin):
    list_display = ("key",)
    search_fields = ("key", "content", "file")

    def get_changeform_initial_data(self, request):
        """Pre-fill the key field when adding a new chunk via URL parameter"""
        initial = super().get_changeform_initial_data(request)
        if 'key' in request.GET:
            initial['key'] = request.GET['key']
        return initial

@admin.register(Expert)
class CallbackExpertAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'photo',)

@admin.register(MinstroyProgram)
class MinstroyProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    list_display_links = ("title",)
    search_fields = ("title", "description")
    ordering = ("id",)

@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "created_at")
    search_fields = ("code", "title")

@admin.register(UnifiedRequest)
class UnifiedRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "colored_type", "phone", "email", "created_at")
    list_filter = ("request_type", "created_at")
    search_fields = ("name", "phone", "email")

    def colored_type(self, obj):
        colors = {
            "callback": "#d97706",
            "noc": "#16a34a",
            "prep_expert": "#6f58f0",
            "prep_specialist": "#2563eb",
        }

        labels = {
            "callback": "Запрос на звонок",
            "noc": "Заявка на НОК",
            "prep_expert": "Подготовка эксперта",
            "prep_specialist": "Подготовка специалиста",
        }

        color = colors.get(obj.request_type, "black")
        text = labels.get(obj.request_type, obj.request_type)

        return format_html(
            '<span style="color: {}; font-weight:600;">{}</span>',
            color,
            text
        )

    colored_type.short_description = "Тип заявки"


