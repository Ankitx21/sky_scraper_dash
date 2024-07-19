from django.contrib import admin
from .models import Website

@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'scraped_articles_24hrs', 'automation_running', 'source_active')
