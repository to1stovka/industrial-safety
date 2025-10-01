from django.contrib import admin
from news.models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at")
    search_fields = ("title", "description")
    list_filter = ("category", "created_at")
