from typing import Any
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from . models import Car, OrderEntry, Service, Order
from django.views import generic

def index(request):
    cars = Car.objects.all().count()
    all_services = Service.objects.all()
    clean_service_names = [service.name for service in all_services]
    services = Service.objects.all().count()
    new_services = OrderEntry.objects.filter(status__exact="new").count()
    processing_services = OrderEntry.objects.filter(status__exact="processing").count()
    completed_services = OrderEntry.objects.filter(status__exact="complete").count()
    canceled_services = OrderEntry.objects.filter(status__exact="cancelled").count()

    context = {
        'cars': cars,
        'services': services,
        'new_services': new_services,
        'processing_services': processing_services,
        'completed_services': completed_services,
        'canceled_services': canceled_services,
        'all_services': clean_service_names,
    }
    return render(request, 'service/index.html', context)

def car_list(request):
    qs = Car.objects
    query = request.GET.get('query')
    if query:
        qs = qs.filter(
            Q(model__year__istartswith=query) |
            Q(model__model__istartswith=query) |
            Q(model__make__istartswith=query) 
            # Q(vin_code__icontains=query)
        )
    else:
        qs = qs.all()
    paginator = Paginator(qs, 2)
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
    return render(request, 'service/order_detail.html', {'order': order})


class OrderListView(generic.ListView):
    model = Order
    paginate_by = 4
    context_object_name = 'orders'
    template_name = 'service/order_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            qs = qs.filter(
                Q(order_entries__price__icontains=query) |
                Q(car__customer__istartswith=query) |
                Q(car__licence_plate__istartswith=query) |
                Q(car__vin_code__istartswith=query) |
                Q(car__model__make__icontains=query)
            )
        return qs
            