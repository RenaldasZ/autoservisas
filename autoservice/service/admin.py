

from django.contrib import admin
from . import models

class CarAdmin(admin.ModelAdmin):
    list_display = [('customer'),('model'),('licence_plate'),('vin_code')]


class OrderAdmin(admin.ModelAdmin):
    list_display = [('car'),('date')]


# Register your models here.
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Car, CarAdmin)
admin.site.register(models.CarModel)
admin.site.register(models.Service)
admin.site.register(models.OrderEntry)
