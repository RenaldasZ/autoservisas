from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CarModel(models.Model):
    make = models.CharField(_("Make"), max_length=100)
    model = models.CharField(_("Model"), max_length=100)
    year = models.PositiveIntegerField(_("Year"))
    engine = models.CharField(_("Engine"), max_length=100)

    class Meta:
        ordering = ["year"]
        verbose_name = _("car model")
        verbose_name_plural = _("car models")

    def __str__(self):
        return f"{self.make} {self.model} ({self.year}) {self.engine}"

    def get_absolute_url(self):
        return reverse("car_model_detail", kwargs={"pk": self.pk})


class Car(models.Model):
    licence_plate = models.CharField(_("Licence Plate"), max_length=20)
    vin_code = models.CharField(_("VIN Code"), max_length=50)
    customer = models.CharField(max_length=50, db_index=True)
    model = models.ForeignKey(
        CarModel, verbose_name=_("model"), related_name="cars", on_delete=models.CASCADE, null=True,)

    class Meta:
        ordering = ["licence_plate"]
        verbose_name = _("car")
        verbose_name_plural = _("cars")

    def __str__(self):
        return self.licence_plate

    def get_absolute_url(self):
        return reverse("car_detail", kwargs={"pk": self.pk})


class Service(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    price = models.DecimalField(_("Price"), max_digits=18, decimal_places=2)

    class Meta:
        ordering = ["name", "id"]
        verbose_name = _("service")
        verbose_name_plural = _("services")

    def __str__(self):
        return self.name


class Order(models.Model):
    date = models.CharField(_("Date"), max_length=50)
    car = models.ForeignKey(
        Car, verbose_name=_("car"), related_name="orders", on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["date", "id"]
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return f"Order #{self.pk}"

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})


class OrderEntry(models.Model):
    service = models.ForeignKey(
        Service, verbose_name=_("service"), related_name="order_entries", on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(
        Order, verbose_name=_("order"), related_name="order_entries", on_delete=models.CASCADE, null=True)

    quantity = models.CharField(_("Quantity"), max_length=50)
    price = models.CharField(_("Price"), max_length=50)

    class Meta:
        verbose_name = _("order entry")
        verbose_name_plural = _("order entries")

    def __str__(self):
        return f"Order entry #{self.pk} Service type: {self.service.name}"

    def get_absolute_url(self):
        return reverse("orderentry_detail", kwargs={"pk": self.pk})