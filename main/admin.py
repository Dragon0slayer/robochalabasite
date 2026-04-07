from django.contrib import admin
from .models import Brand, Flavor, Chips


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')


class FlavorAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')


class ChipsAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'created_at', 'updated_at')


admin.site.register(Brand, BrandAdmin)
admin.site.register(Flavor, FlavorAdmin)
admin.site.register(Chips, ChipsAdmin)