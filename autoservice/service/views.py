from django.shortcuts import render
from . models import Car, OrderEntry, Service

def index(request):
    num_cars = Car.objects.all().count()
    num_services = Service.objects.all().count()
    num_completed_services = OrderEntry.objects.filter(status__exact="complete").count()

    context = {
        'num_cars': num_cars,
        'num_services': num_services,
        'num_completed_services': num_completed_services,
    }

    return render(request, 'service/index.html', context)
