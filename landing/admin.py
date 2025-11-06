from django.contrib import admin
from landing.models import (CourseDirection,
                            Review,
                            Chunk, 
                            CallbackRequest, 
                            Expert, 
                            NOCRequest, 
                            MinstroyProgram,
                            Qualification
                            )

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
    search_fields = ("key", "content")

    def get_changeform_initial_data(self, request):
        """Pre-fill the key field when adding a new chunk via URL parameter"""
        initial = super().get_changeform_initial_data(request)
        if 'key' in request.GET:
            initial['key'] = request.GET['key']
        return initial
    
@admin.register(CallbackRequest)
class CallbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at',)

@admin.register(Expert)
class CallbackExpertAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'photo',)

@admin.register(NOCRequest)
class NOCRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'file', 'created_at')

@admin.register(MinstroyProgram)
class MinstroyProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("title",)
    search_fields = ("title", "description")

@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "created_at")
    search_fields = ("code", "title")