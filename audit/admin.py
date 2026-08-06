from django.contrib import admin
from .models import WebsiteAnalysis


@admin.register(WebsiteAnalysis)
class WebsiteAnalysisAdmin(admin.ModelAdmin):

    list_display = (
        "url",
        "seo_score",
        "status_code",
        "created_at",
    )

    search_fields = (
        "url",
        "title",
    )