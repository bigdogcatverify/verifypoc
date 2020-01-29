import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import LivingItem, WorkItem
from .forms import EnterLivingForm, EnterWorkForm


@login_required
def hello_world(request):
    return render(request, 'home.html')


class EventListView(LoginRequiredMixin, generic.ListView):
    model = LivingItem
    context_object_name = 'my_event_list'

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        context.update({
            'work_history_list': WorkItem.objects.all(),
        })

        return context

    def get_queryset(self):
        return LivingItem.objects.all()


@login_required
def add_event(request):

    if request.method == 'POST':

        form = EnterLivingForm(request.POST)

        if form.is_valid():
            new_item = LivingItem()
            new_item.start_date = form.cleaned_data['start_date']
            new_item.end_date = form.cleaned_data['end_date']
            new_item.address = form.cleaned_data['address']
            new_item.verifier = form.cleaned_data['verifier']
            new_item.save()

            return HttpResponseRedirect(reverse('hello_world'))

    else:
        form = EnterLivingForm()

    context = {
        'form': form
    }

    return render(request, 'verify/event_added.html', context)


@login_required
def add_work_event(request):

    if request.method == 'POST':

        form = EnterWorkForm(request.POST)

        if form.is_valid():
            new_item = WorkItem()
            new_item.start_date = form.cleaned_data['start_date']
            new_item.end_date = form.cleaned_data['end_date']
            new_item.work_place = form.cleaned_data['work_place']
            new_item.verifier = form.cleaned_data['verifier']
            new_item.save()

            return HttpResponseRedirect(reverse('hello_world'))

    else:
        form = EnterWorkForm()

    context = {
        'form': form
    }

    return render(request, 'verify/event_added.html', context)
