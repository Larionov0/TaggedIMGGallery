from django.contrib import admin
from .models import  *

from django.utils.html import format_html


class ImagePartInline(admin.TabularInline):  # або можна використати admin.StackedInline для іншого формату відображення
    model = ImagePart
    extra = 1  # Це кількість нових форм, які будуть відображатися за замовчуванням для нового ImagePart


class CardAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'display_image')
    readonly_fields = ('display_image',)
    inlines = [
        ImagePartInline,
    ]

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        elif obj.video:
            return format_html('<video width="50" height="50" autoplay loop muted><source src="{}" type="video/mp4"></video>', obj.video.url)
        else:
            return 'No image or video'
    display_image.short_description = 'Img'


admin.site.register(Card, CardAdmin)

for model in [Tag, TagType, ImagePart]:
    admin.site.register(model)
