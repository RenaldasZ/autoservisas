from django.shortcuts import render
from . models import Car, OrderEntry, Service

def index(request):
    cars = Car.objects.all().count()
    services = Service.objects.all().count()
    completed_services = OrderEntry.objects.filter(status__exact="complete").count()

    context = {
        'cars': cars,
        'services': services,
        'completed_services': completed_services,
    }

    return render(request, 'service/index.html', context)
