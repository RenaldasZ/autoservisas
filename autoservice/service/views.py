

from typing import Any, Dict, Optional, Type
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.db.models import Q
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.utils.translation import gettext_lazy as _
from . models import Car, OrderEntry, Service, Order
from django.views import generic
from . forms import OrderReviewForm, OrderForm, CarForm
from django.urls import reverse_lazy


def index(request):
    cars = Car.objects.all().count()
    all_services = Service.objects.all()
    clean_service_names = [service.name for service in all_services]
    services = Service.objects.all().count()
    new_services = OrderEntry.objects.filter(status__exact="new").count()
    processing_services = OrderEntry.objects.filter(status__exact="processing").count()
    completed_services = OrderEntry.objects.filter(status__exact="complete").count()
    canceled_services = OrderEntry.objects.filter(status__exact="cancelled").count()

    #apsilankymu skaitliukas
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'cars': cars,
        'services': services,
        'new_services': new_services,
        'processing_services': processing_services,
        'completed_services': completed_services,
        'canceled_services': canceled_services,
        'all_services': clean_service_names,
        'num_visits': num_visits,
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
            


class OrderDetailView(generic.edit.FormMixin, generic.DetailView):
    model = Order
    template_name = 'service/order_detail.html'
    form_class = OrderReviewForm

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['order'] = self.get_object()
        initial['reviewer'] = self.request.user
        return initial
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form: Any) -> HttpResponse:
        form.instance.order = self.get_object()
        form.instance.reviewer = self.request.user
        form.save()
        messages.success(self.request, _('Review posted!'))
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('order_detail', kwargs={'pk':self.get_object().pk})
    

class UserOrdersListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'service/user_orders.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(car__client=self.request.user).order_by('due_back')
        return qs


class UserCarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    template_name = 'service/user_car_list.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(client=self.request.user)
        return qs


class UserOrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = 'user_order.html'


class UserOrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'service/user_order_create.html'  

    def get_form(self, form_class: Type[BaseModelForm] | None = form_class) -> BaseModelForm:
        form = super().get_form(form_class)
        if not form.is_bound:
            form.fields["car"].queryset = Car.objects.filter(client=self.request.user)
        return form

    def get_success_url(self) -> str:
        return reverse('my_orders')

    # def form_valid(self, form):
    #     form.instance.client = self.request.user
    #     return super().form_valid(form)

    def get_absolute_url(self):
        return reverse('order_detail', args=[str(self.id)])
    

class UserCarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm
    template_name = 'service/user_car_create.html'  

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['client'] = self.request.user
        return initial
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.client = self.request.user
        return super().form_valid(form)
    

class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'service/user_car_update.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.client = self.request.user
        return super().form_valid(form)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.client != self.request.user:
            raise get_object_or_404()
        return obj

    def get_success_url(self):
        return reverse('car_detail', kwargs={'pk': self.object.pk})
    

class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Order
    template_name = 'service/order_confirm_delete.html'
    
    def test_func(self):
        order = self.get_object() 
        proccesing_or_complete = order.order_entries.filter(Q(status='processing') | Q(status='complete')).exists()
        return order.car.client == self.request.user and not proccesing_or_complete

    def handle_no_permission(self):
        messages.error(self.request, _('You cannot delete the Order while it is already in process or complete. If you still want to delete your order, please contact the garage staff! Or You are not authorized'))
        return redirect('my_orders')
    
    def get_success_url(self):
        messages.success(self.request, _('Order delete success!'))
        return reverse_lazy('my_orders')
    