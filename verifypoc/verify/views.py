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

from .models import (LivingItem, WorkItem,
                     User, Profile,
                     Businesses, Actions,
                     EducationItem)
from .forms import (EnterLivingForm, EnterWorkForm, UserForm,
                    ProfileForm, RequesterSignUpForm, VerifierSignUpForm,
                    ShareWithForm, EnterEducationForm)


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
            'education_history_list': EducationItem.objects.all(),
        })

        return context

    def get_queryset(self):
        return LivingItem.objects.all()


class ShareWithView(LoginRequiredMixin, generic.ListView):
    model = LivingItem
    context_object_name = 'my_event_list'
    template_name = 'verify/share_list.html'

    def get_context_data(self, **kwargs):
        context = super(ShareWithView, self).get_context_data(**kwargs)
        context.update({
            'work_history_list': WorkItem.objects.all(),
            'education_history_list': EducationItem.objects.all(),
        })

        return context

    def get_queryset(self):
        return LivingItem.objects.all()


@login_required()
def share(request, pk):
    if request.method == 'POST':
        form = ShareWithForm(request.POST)
        if form.is_valid():
            item = LivingItem.objects.get(id=pk)
            item.shared_with = form.cleaned_data['share_with']
            user = User.objects.get(id=request.user.id)
            item.action.create(action_type=Actions.SHARE_EVENT,
                               user=user)
            item.save()
        return redirect('hello_world')
    else:
        item = LivingItem.objects.get(id=pk)
        form = ShareWithForm()
    return render(request, 'verify/share.html',
                  {'object': item,
                   'form': form})


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
            user = User.objects.get(id=request.user.id)
            new_item.added_by = user
            new_item.action.create(action_type=Actions.ADD_LIVING_EVENT,
                                   user=user)
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
            user = User.objects.get(id=request.user.id)
            new_item.added_by = user
            new_item.action.create(action_type=Actions.ADD_WORK_EVENT,
                                   user=user)
            new_item.save()

            return HttpResponseRedirect(reverse('hello_world'))

    else:
        form = EnterWorkForm()

    context = {
        'form': form
    }

    return render(request, 'verify/event_added.html', context)


@login_required
def add_education_event(request):

    if request.method == 'POST':

        form = EnterEducationForm(request.POST)

        if form.is_valid():
            new_item = EducationItem()
            new_item.start_date = form.cleaned_data['start_date']
            new_item.end_date = form.cleaned_data['end_date']
            new_item.institution = form.cleaned_data['institution']
            new_item.verifier = form.cleaned_data['verifier']
            user = User.objects.get(id=request.user.id)
            new_item.added_by = user
            new_item.action.create(action_type=Actions.ADD_EDUCATION_EVENT,
                                   user=user)
            new_item.save()

            return HttpResponseRedirect(reverse('hello_world'))

    else:
        form = EnterEducationForm()

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
    return render(request, 'verify/profile.html', {
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


class RequesterSignUpView(generic.CreateView):
    model = User
    form_class = RequesterSignUpForm
    template_name = 'registration/signup_form.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'requester'
        return super().get_context_data(**kwargs)

    def from_valid(self, form):
        user = form.save()


class VerifierSignUpView(generic.CreateView):
    model = User
    form_class = VerifierSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'verifier'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        business = Businesses()
        business.business_name = form.cleaned_data['business_name']
        business.business_type = form.cleaned_data['business_type']
        business.save()
        user = form.save()
        return redirect('hello_world')


class StandardSignUpView(generic.TemplateView):
    template_name = 'registration/signup.html'


class RequesterListView(LoginRequiredMixin, generic.ListView):
    model = LivingItem
    context_object_name = 'my_event_list'
    template_name = 'verify/requester_list.html'

    def get_context_data(self, **kwargs):
        context = super(RequesterListView, self).get_context_data(**kwargs)
        context.update({
            'work_history_list': WorkItem.objects.filter(is_verified=False,
                                                         verifier__business_name=self.request.user.business_name),
            'education_history_list': EducationItem.objects.filter(is_verified=False,
                                                                   verifier__business_name=self.request.user.business_name),
        })

        return context

    def get_queryset(self):
        return LivingItem.objects.filter(is_verified=False,
                                         verifier__business_name=self.request.user.business_name)


@login_required()
def verify_event(request, pk):
    if request.method == 'POST':
        item = LivingItem.objects.get(id=pk)
        item.is_verified = True
        user = User.objects.get(id=request.user.id)
        item.action.create(action_type=Actions.VERIFY_EVENT,
                           user=user)
        item.save()
        return redirect('hello_world')
    else:
        item = LivingItem.objects.get(id=pk)
    return render(request, 'verify/update.html',
                  {'object': item})


class ReviewListView(LoginRequiredMixin, generic.ListView):
    model = LivingItem
    context_object_name = 'my_event_list'
    template_name = 'verify/reviewer_list.html'

    def get_context_data(self, **kwargs):
        context = super(ReviewListView, self).get_context_data(**kwargs)
        context.update({
            'work_history_list': WorkItem.objects.filter(shared_with__business_name=self.request.user.business_name),
            'education_history_list': EducationItem.objects.filter(is_verified=False,
                                                                   verifier__business_name=self.request.user.business_name),
        })

        return context

    def get_queryset(self):
        return LivingItem.objects.filter(shared_with__business_name=self.request.user.business_name)


class ActionsListView(LoginRequiredMixin, generic.ListView):
    model = Actions
    context_object_name = 'my_actions_list'
    template_name = 'verify/actions_list.html'

    def get_queryset(self):
        return Actions.objects.filter(user=self.request.user.id)
