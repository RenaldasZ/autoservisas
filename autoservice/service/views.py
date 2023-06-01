

from django.shortcuts import render, get_object_or_404
from . models import Car, OrderEntry, Service, Order
from django.views.generic import ListView

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

def car_list(request):
    cars = Car.objects.all()
    return render(request, 'service/car_list.html', {'cars': cars})

def car_detail(request, pk: int):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'service/car_detail.html', {'car': car})

def order_detail(request, pk: int):
    order = get_object_or_404(Order, pk=pk)
    total_price = sum(entry.price for entry in order.order_entries.all())

    return render(request, 'service/order_detail.html', {'order': order, 'total_price': total_price})


class OrderListView(ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'service/order_list.html'

