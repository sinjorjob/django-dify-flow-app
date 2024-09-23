from django.contrib import admin
from .models import Category, Subcategory

class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory_count')
    search_fields = ('name',)
    inlines = [SubcategoryInline]

    def subcategory_count(self, obj):
        return obj.subcategory_set.count()
    subcategory_count.short_description = 'サブカテゴリ数'

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')