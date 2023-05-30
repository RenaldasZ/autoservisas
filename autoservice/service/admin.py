from django.contrib import admin
from . import models
from .models import OrderEntry

class OrderEntryInline(admin.TabularInline):
    model = OrderEntry

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "car", "date")
    inlines = [OrderEntryInline]

class CarAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "model", "licence_plate", "vin_code")
    list_filter = ("customer", "model" )
    search_fields = ('licence_plate', 'vin_code')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price")

# Register your models here.
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Car, CarAdmin)
admin.site.register(models.CarModel)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.OrderEntry)
