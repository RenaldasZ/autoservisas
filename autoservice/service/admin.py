from django.contrib import admin
from . import models


class CarModelAdmin(admin.ModelAdmin):
    list_display = ("id", "make", "model", "year", "engine")


class CarAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "model", "licence_plate", "vin_code")
    list_filter = ("customer", "model")
    search_fields = ('licence_plate', 'vin_code')


class OrderEntryInline(admin.TabularInline):
    model = models.OrderEntry
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "car", "price")
    inlines = [OrderEntryInline]


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price")


# Register your models here.
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Car, CarAdmin)
admin.site.register(models.CarModel, CarModelAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.OrderEntry)
