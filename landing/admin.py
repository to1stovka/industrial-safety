from django.contrib import admin
from landing.models import (CourseDirection,
                            Review,
                            Chunk, 
                            Expert, 
                            MinstroyProgram,
                            Qualification,
                            UnifiedRequest,
                            ThreedGalleryImage,
                            NocPreparationDirection,
                            NocMailSettings,
                            )
from django.utils.html import format_html
from django.utils.html import mark_safe

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
    list_display = ("name", "colored_type", "phone", "email", "has_file", "has_consent_file", "created_at")
    list_filter = ("request_type", "created_at")
    search_fields = ("name", "phone", "email")
    readonly_fields = ("file", "consent_file", "created_at")

    def has_file(self, obj):
        return bool(obj.file)
    has_file.short_description = "Есть файл заявки"
    has_file.boolean = True

    def has_consent_file(self, obj):
        return bool(obj.consent_file)
    has_consent_file.short_description = "Есть согласие"
    has_consent_file.boolean = True

    def colored_type(self, obj):
        colors = {
            "callback": "#d97706",
            "noc": "#16a34a",
            "prep_expert": "#6f58f0",
            "prep_specialist": "#2563eb",
            "noc_signed": "#f02222"
        }

        labels = {
            "callback": "Запрос на звонок",
            "noc": "Универсальная заявка",
            "prep_expert": "Подготовка эксперта",
            "prep_specialist": "Подготовка специалиста",
            "noc_signed": "Подписанная заявка НОК"
        }

        color = colors.get(obj.request_type, "black")
        text = labels.get(obj.request_type, obj.request_type)

        return format_html(
            '<span style="color: {}; font-weight:600;">{}</span>',
            color,
            text
        )

    colored_type.short_description = "Тип заявки"


@admin.register(ThreedGalleryImage)
class ThreedGalleryImageAdmin(admin.ModelAdmin):
    list_display = ("id", "preview")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="120" style="border-radius:8px;">')
        return "Нет изображения"

    preview.short_description = "Превью"
    
@admin.register(NocPreparationDirection)
class NocPreparationDirectionAdmin(admin.ModelAdmin):
    list_display = ("title", "kind", "track", "category", "code", "is_active", "created_at")
    list_filter = ("kind", "is_active", "track", "category")
    search_fields = ("title", "code")
    ordering = ("kind", "id")


@admin.register(NocMailSettings)
class NocMailSettingsAdmin(admin.ModelAdmin):
    list_display = ("__str__", "updated_at")
    readonly_fields = ("admin_hint",)
    fields = ("admin_hint", "to_emails", "cc_emails")

    def admin_hint(self, obj=None):
        return format_html(
            "Если поля пустые, письмо отправится на ucbp@yandex.ru и ucbp@bezopprom.ru.<br>"
            "Если заполнен только основной получатель, письмо уйдёт только ему."
        )
    admin_hint.short_description = "Примечание"

    def has_add_permission(self, request):
        return not NocMailSettings.objects.exists()