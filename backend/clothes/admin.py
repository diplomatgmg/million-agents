from django.contrib import admin

from .models import Cloth, ClothPrice


@admin.register(Cloth)
class ClothAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "color",
        "width",
        "composition",
        "density",
        "length",
        "country",
    )
    list_filter = ("color", "country")
    search_fields = ("name", "description", "composition", "country")
    list_per_page = 50


@admin.register(ClothPrice)
class ClothPriceAdmin(admin.ModelAdmin):
    list_display = ("cloth_name", "cloth_article", "price", "date_updated")
    list_select_related = ("cloth",)
    list_per_page = 50

    def cloth_name(self, obj):
        return obj.cloth.name

    cloth_name.short_description = "Ткань"

    def cloth_article(self, obj):
        return obj.cloth.article

    cloth_article.short_description = "Артикль"
