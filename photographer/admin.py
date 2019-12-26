from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.

class PhotoInline(admin.TabularInline):

    model = models.Photo


@admin.register(models.Photographer)
class PhotographerAdmin(admin.ModelAdmin):

    """ Photographer Admin Definition """

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "user info",
            {"fields": ("zzigsa", "profile", "introduction", "sns")},
        ),
        (
            "equipment",
            {"fields": ("equip", "equip_picture")},
        ),
        (
            "product info",
            {"fields": ("title", "description", "location")},
        ),
    )

    list_display = (
        "zzigsa",
        "title",
        "location",
        "equip",
        "sns",
        "count_photos",
    )

    list_filter = (
        "zzigsa__zzigsa",
    )

    def count_photos(self, obj):
        return obj.photos.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = ('get_thumbnail',)

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="60px" src="{obj.file.url}" />')

    get_thumbnail.short_description = 'thumbnail'