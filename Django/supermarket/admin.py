from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Status)
admin.site.register(Unit)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
  list_display = ('itemName', 'id', 'display_category', 'qr_code', 'unit')


@admin.register(ItemInstance)
class ItemInstanceAdmin(admin.ModelAdmin):
  list_display = ('instanceName', 'instanceId', 'status', 'expiry_date', 'production_date', 'quantity')
  list_filter = ('instanceName',)
