from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Book, Author, Genre

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'year', 'image_tag')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return mark_safe('<img src="{}" style="max-height: 100px; max-width: 100px;" />'.format(obj.image.url))
        return None
    image_tag.short_description = 'Image'

# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Genre)
