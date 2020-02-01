import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from .models import LivingItem, WorkItem, User, Profile
from .forms import EnterLivingForm, EnterWorkForm, UserForm, ProfileForm


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


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Profile successfully updated'))
            return redirect('hello_world')
        else:
            messages.error(request, _('Please fix the errors'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'verify/profile.html' , {
        'user_form': user_form,
        'profile_form': profile_form
    })


class ProfileListView(LoginRequiredMixin, generic.ListView):
    model = User
    context_object_name = 'my_profile_list'
    template_name = 'verify/profile_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileListView, self).get_context_data(**kwargs)
        context.update({
            'profile_list': Profile.objects.all(),
        })

        return context

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)
