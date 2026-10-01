from django.contrib import admin
from .models import VKPost


@admin.register(VKPost)
class VKPostAdmin(admin.ModelAdmin):
    list_display = ('vk_id', 'created', 'short_text', 'tag_list') 
    search_fields = ('text', 'vk_id')
    list_filter = ('created', 'tags')

    def short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    short_text.short_description = 'Текст'

    def tag_list(self, obj):  
        return ', '.join(t.name for t in obj.tags.all())
    tag_list.short_description = 'Теги'