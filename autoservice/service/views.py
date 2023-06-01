from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from . models import Car, OrderEntry, Service, Order
from django.views import generic

def index(request):
    cars = Car.objects.all().count()
    services = Service.objects.all().count()
    new_services = OrderEntry.objects.filter(status__exact="new").count()
    processing_services = OrderEntry.objects.filter(status__exact="processing").count()
    completed_services = OrderEntry.objects.filter(status__exact="completed").count()
    canceled_services = OrderEntry.objects.filter(status__exact="canceled").count()

    context = {
        'cars': cars,
        'services': services,
        'new_services': new_services,
        'processing_services': processing_services,
        'completed_services': completed_services,
        'canceled_services': canceled_services,
    }
    return render(request, 'service/index.html', context)

def car_list(request):
    paginator = Paginator(Car.objects.all(), 4)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    context = {
        'cars': paged_cars
    }
    return render(request, 'service/car_list.html', context=context)

def car_detail(request, pk: int):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'service/car_detail.html', {'car': car})

def order_detail(request, pk: int):
    order = get_object_or_404(Order, pk=pk)
    total_price = sum(entry.price for entry in order.order_entries.all())

    return render(request, 'service/order_detail.html', {'order': order, 'total_price': total_price})


class OrderListView(generic.ListView):
    model = Order
    paginate_by = 4
    context_object_name = 'orders'
    template_name = 'service/order_list.html'
