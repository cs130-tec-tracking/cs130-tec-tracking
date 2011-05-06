from django.contrib import admin
from models import Asset, Category, AssetCategory, Note

class AssetCategoryInline(admin.TabularInline):
    model = AssetCategory
    extra = 1

class AssetAdmin(admin.ModelAdmin):
    list_display = ('serial_num', 'bar_code', 'rfid', 'asset_model_mfg', 'asset_model_type', 'asset_model_name', 'amt_memory', 'num_cores',)
    list_filter = ('categories__name', 'asset_model_mfg', 'asset_model_type',)
    search_fields = ('serial_num', 'bar_code', 'categories__name', 'asset_model_mfg', 'asset_model_type', 'asset_model_name',)
    inlines = (AssetCategoryInline,)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = (AssetCategoryInline,)

class NoteAdmin(admin.ModelAdmin):
    list_display = ('asset', 'message',)

admin.site.register(Asset, AssetAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Note, NoteAdmin)
