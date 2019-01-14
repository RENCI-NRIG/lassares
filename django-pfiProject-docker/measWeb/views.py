from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from measWeb.models import Measurement
from measWeb.forms import MeasurementForm 
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin
from django.views import View
from measWeb.push import push_measurement_to_elk_stack
from django.contrib.auth.mixins import LoginRequiredMixin

class MeasList(ListView): 
    model = Measurement 
    template_name = "measWeb/measurement_list.html"

class MeasChange(FormMixin, MultipleObjectMixin, View): 
    model = Measurement 
    form_class = MeasurementForm 
    template_name = "measWeb/measurement_list.html"
    success_url = reverse_lazy('measWeb:measurement_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        list_of_ids=request.POST.getlist('_selected_action')
        action=request.POST.get('action')
        print (list_of_ids)
        for obj in self.get_queryset():
            if str(obj.id) in list_of_ids:
                if action == 'delete':
                    return redirect(reverse_lazy('measWeb:measurement_delete',  kwargs={'pk': obj.id})) 
                if action == 'push':
                #if action == 'push' and obj.status != 'p':
                    if push_measurement_to_elk_stack(obj):
                        obj.status = 'p'
                        obj.save()
        return redirect(self.get_success_url()) 

class MeasChangeList(LoginRequiredMixin, View):
    template_name = "measWeb/measurement_list.html"

    def get(self, request, *args, **kwargs):
        view = MeasList.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = MeasChange.as_view()
        return view(request, *args, **kwargs)

class MeasCreate(LoginRequiredMixin, CreateView): 
    model = Measurement 
    form_class = MeasurementForm 
    success_url = reverse_lazy('measWeb:measurement_list')

class MeasUpdate(LoginRequiredMixin, UpdateView): 
    model = Measurement 
    form_class = MeasurementForm 
    success_url = reverse_lazy('measWeb:measurement_list')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        if 'delete' in self.request.POST:
            return redirect(reverse_lazy('measWeb:measurement_delete',  kwargs={'pk': self.object.id})) 
        form.save()
        return super().form_valid(form)

class MeasDelete(LoginRequiredMixin, DeleteView): 
    model = Measurement 
    success_url = reverse_lazy('measWeb:measurement_list')

@login_required
def index(request):
    return render(request, 'measWeb/index.html')
