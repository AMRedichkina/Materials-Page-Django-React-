from django.contrib import admin
from .models import Material


class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'description', 'amount', 'availability', 'type')


admin.site.register(Material, MaterialAdmin)
