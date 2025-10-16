from django.contrib import admin
from landing.models import CourseDirection, Review

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