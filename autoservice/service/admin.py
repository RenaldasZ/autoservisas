from django.contrib import admin
from . import models


class CarModelAdmin(admin.ModelAdmin):
    list_display = ("id", "make", "model", "year", "engine")


class CarAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "model", "licence_plate", "vin_code", "note")
    list_filter = ("note", "model")
    search_fields = ('licence_plate', 'vin_code')


class OrderEntryInline(admin.TabularInline):
    model = models.OrderEntry
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "car", "price", "client")
    inlines = [OrderEntryInline]


class OrderEntryAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'service')
    list_filter = ('order', 'status')
    list_editable = ('status', )


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price")


class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewed_at', 'order', 'reviewer', 'content')


# Register your models here.
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Car, CarAdmin)
admin.site.register(models.CarModel, CarModelAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.OrderEntry, OrderEntryAdmin)
admin.site.register(models.OrderReview, OrderReviewAdmin)
