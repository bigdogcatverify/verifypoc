import os
import requests
import hashlib
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from .models import (Item, Requests,
                     User, Profile,
                     Businesses, Actions, Document)
from .forms import (EnterLivingForm, EnterWorkForm, UserForm,
                    ProfileForm, RequesterSignUpForm, VerifierSignUpForm,
                    ShareWithForm, EnterEducationForm, DocumentForm,
                    LinkWithForm, RequestForm, RequestWithForm)

block_endpoint = os.getenv('BLOCK_ENDPOINT', 'http://127.0.0.1:8000')

@login_required
def hello_world(request):
    return render(request, 'home.html')


class EventListView(LoginRequiredMixin, generic.ListView):
    model = Item
    context_object_name = 'my_event_list'
    template_name = 'verify/livingitem_list.html'

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        full_list = Item.objects.filter(added_by=self.request.user.id).count()
        verified_list = Item.objects.filter(added_by=self.request.user.id,
                                            is_verified=True).count()
        score = workout_score(full_list, verified_list)
        context.update({
            'work_history_list': Item.objects.filter(event_type='work',
                                                     added_by=self.request.user.id),
            'education_history_list': Item.objects.filter(event_type='education',
                                                          added_by=self.request.user.id),
            'score': score
        })

        return context

    def get_queryset(self):
        return Item.objects.filter(event_type='living',
                                   added_by=self.request.user.id)


def workout_score(number_of_requests, number_verified):
    """Workout from number of requests their score and status"""
    if number_of_requests == 0:
        score = 0
    else:
        score = int(number_verified / number_of_requests * 100)
    score_map = {'very_good': 'Very Good',
                 'good': 'Good',
                 'average': 'Average',
                 'could_do_better': 'Could do Better'}
    if score > 80:
        return score_map['very_good'], score
    elif score > 60:
        return score_map['good'], score
    elif score > 40:
        return score_map['average'], score
    else:
        return score_map['could_do_better'], score


class ShareWithView(LoginRequiredMixin, generic.ListView):
    model = Item
    context_object_name = 'my_event_list'
    template_name = 'verify/share_list.html'

    def get_context_data(self, **kwargs):
        context = super(ShareWithView, self).get_context_data(**kwargs)
        context.update({
            'work_history_list': Item.objects.filter(event_type='work'),
            'education_history_list': Item.objects.filter(event_type='education'),
        })

        return context

    def get_queryset(self):
        return Item.objects.filter(event_type='living')


@login_required()
def share(request, pk):
    if request.method == 'POST':
        form = ShareWithForm(request.POST)
        if form.is_valid():
            item = Item.objects.get(id=pk)
            item.shared_with = form.cleaned_data['share_with']
            user = User.objects.get(id=request.user.id)
            item.action.create(action_type=Actions.SHARE_EVENT,
                               user=user)
            item.save()
        return redirect('hello_world')
    else:
        item = Item.objects.get(id=pk)
        form = ShareWithForm()
    return render(request, 'verify/share.html',
                  {'object': item,
                   'form': form})


@login_required
def add_event(request):

    if request.method == 'POST':

        form = EnterLivingForm(request.POST)

        if form.is_valid():
            new_item = Item()
            new_item.start_date = form.cleaned_data['start_date']
            new_item.end_date = form.cleaned_data['end_date']
            new_item.address = form.cleaned_data['address']
            new_item.verifier = form.cleaned_data['verifier']
            user = User.objects.get(id=request.user.id)
            new_item.added_by = user
            new_item.event_type = 'living'
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
            new_item = Item()
            new_item.start_date = form.cleaned_data['start_date']
            new_item.end_date = form.cleaned_data['end_date']
            new_item.address = form.cleaned_data['work_place']
            new_item.verifier = form.cleaned_data['verifier']
            user = User.objects.get(id=request.user.id)
            new_item.added_by = user
            new_item.event_type = 'work'
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
            new_item = Item()
            new_item.start_date = form.cleaned_data['start_date']
            new_item.end_date = form.cleaned_data['end_date']
            new_item.address = form.cleaned_data['institution']
            new_item.verifier = form.cleaned_data['verifier']
            user = User.objects.get(id=request.user.id)
            new_item.added_by = user
            new_item.event_type = 'education'
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
    model = Item
    context_object_name = 'my_event_list'
    template_name = 'verify/requester_list.html'

    def get_context_data(self, **kwargs):
        context = super(RequesterListView, self).get_context_data(**kwargs)
        context.update({
            'work_history_list': Item.objects.filter(is_verified=False,
                                                     verifier__business_name=self.request.user.business_name,
                                                     event_type='work'),
            'education_history_list': Item.objects.filter(is_verified=False,
                                                          verifier__business_name=self.request.user.business_name,
                                                          event_type='education'),
        })

        return context

    def get_queryset(self):
        return Item.objects.filter(is_verified=False,
                                   verifier__business_name=self.request.user.business_name,
                                   event_type='living')


@login_required()
def verify_event(request, pk):
    if request.method == 'POST':
        item = Item.objects.get(id=pk)
        item.is_verified = True
        user = User.objects.get(id=request.user.id)
        item.verified_by = Businesses.objects.get(business_name=request.user.business_name)
        item.verified_unique_id = request.user.unique_id
        request_username = User.objects.get(username=item.added_by)
        url = '%s/mine_block' % block_endpoint
        verify_data = {'requester': request_username.unique_id,
                       'verifier': request.user.unique_id,
                       'address': item.address,
                       'isverified': True}
        try:
            verify_request = requests.post(url, json=verify_data)
        except requests.exceptions.HTTPError as err:
            raise err
        json_obj = verify_request.json()
        item.verified_hash = json_obj['nonce']
        item.chain_index = json_obj['index']
        item.verified_datetime = json_obj['timestamp']
        item.action.create(action_type=Actions.VERIFY_EVENT,
                           user=user)
        item.save()
        return redirect('hello_world')
    else:
        item = Item.objects.get(id=pk)
    return render(request, 'verify/update.html',
                  {'object': item})


@login_required()
def validate_event_chain(request, pk):
    if request.method == 'POST':
        item = Item.objects.get(id=pk)
        url = '%s/get_chain' % block_endpoint
        try:
            verify_request = requests.get(url)
        except requests.exceptions.HTTPError as err:
            raise err
        json_obj = verify_request.json()
        index = item.chain_index
        chain_block = json_obj['chain'][index - 1]
        chain_nonce = chain_block['nonce']
        previous_block = json_obj['chain'][index - 2]
        previous_nonce = previous_block['nonce']
        is_verified = item.is_verified
        if is_verified == 1:
            is_verified = 'true'
        address = item.address
        requester = request.user.unique_id
        verifier = item.verified_unique_id
        string_for_hash = requester + verifier + is_verified + address + str(previous_nonce)
        hash_operation = hashlib.sha256(str(string_for_hash).encode()).hexdigest()
        try:
            assert hash_operation == chain_nonce
            return render(request, 'verify/success.html')
        except AssertionError as err:
            raise err
            return render(request, 'verify/failure.html')
    else:
        item = Item.objects.get(id=pk)
    return render(request, 'verify/validate.html',
                  {'object': item})


class ReviewListView(LoginRequiredMixin, generic.ListView):
    model = Item
    context_object_name = 'my_event_list'
    template_name = 'verify/reviewer_list.html'

    def get_context_data(self, **kwargs):
        context = super(ReviewListView, self).get_context_data(**kwargs)
        context.update({
            'work_history_list': Item.objects.filter(shared_with__business_name=self.request.user.business_name,
                                                     event_type='work'),
            'education_history_list': Item.objects.filter(shared_with__business_name=self.request.user.business_name,
                                                                   event_type='education'),
            'document_list': Document.objects.filter(shared_with__business_name=self.request.user.business_name)
        })

        return context

    def get_queryset(self):
        return Item.objects.filter(shared_with__business_name=self.request.user.business_name,
                                   event_type='living')


class ActionsListView(LoginRequiredMixin, generic.ListView):
    model = Actions
    context_object_name = 'my_actions_list'
    template_name = 'verify/actions_list.html'

    def get_queryset(self):
        return Actions.objects.filter(user=self.request.user.id)


def upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            user = User.objects.get(id=request.user.id)
            document.user = user
            document.action.create(action_type=Actions.ADD_DOCUMENT_EVENT,
                                   user=user)
            document.save()
            return redirect('hello_world')
    else:
        form = DocumentForm()

    return render(request, 'verify/file_upload.html', {
        'form': form
    })


class DocumentView(LoginRequiredMixin, generic.ListView):
    model = Document
    context_object_name = 'document_list'
    template_name = 'verify/document_share_list.html'

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)


@login_required()
def document_share(request, pk):
    if request.method == 'POST':
        form = ShareWithForm(request.POST)
        if form.is_valid():
            item = Document.objects.get(id=pk)
            item.shared_with = form.cleaned_data['share_with']
            user = User.objects.get(id=request.user.id)
            item.action.create(action_type=Actions.SHARE_EVENT,
                               user=user)
            item.save()
        return redirect('hello_world')
    else:
        item = Document.objects.get(id=pk)
        form = ShareWithForm()
    return render(request, 'verify/document_share.html',
                  {'object': item,
                   'form': form})


@login_required()
def document_link(request, pk):
    if request.method == 'POST':
        form = LinkWithForm(request.POST, user=User.objects.get(id=request.user.id))
        if form.is_valid():
            item = Document.objects.get(id=pk)
            user = User.objects.get(id=request.user.id)
            link_item = Item.objects.get(address=form.cleaned_data['link_with'],
                                         added_by=user)
            user = User.objects.get(id=request.user.id)
            link_item.linked_docs = item
            link_item.save()
            item.action.create(action_type=Actions.SHARE_EVENT,
                               user=user)
        return redirect('hello_world')
    else:
        user = User.objects.get(id=request.user.id)
        item = Document.objects.get(id=pk)
        form = LinkWithForm(user=user)
    return render(request, 'verify/document_link.html',
                  {'object': item,
                   'form': form})


def view_document(request, pk):
    path = str(Document.objects.get(id=pk).document)
    file_path = os.path.join(settings.MEDIA_URL, path)
    context = {'image': file_path}
    return render(request, "verify/view_images.html", context)


@login_required()
def request_info(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            item = Requests()
            user = User.objects.get(id=request.user.id)
            item.user = form.cleaned_data['user']
            item.start_date = form.cleaned_data['start_date']
            item.end_date = form.cleaned_data['end_date']
            item.requester = user
            item.save()
        return redirect('hello_world')
    else:
        form = RequestForm()
    return render(request, 'verify/request_info.html',
                  {'form': form})


class RequestListView(LoginRequiredMixin, generic.ListView):
    model = Requests
    context_object_name = 'my_request_list'
    template_name = 'verify/request_list.html'

    def get_queryset(self):
        return Requests.objects.filter(user=self.request.user.id)


@login_required()
def request_info_list(request, pk):
    if request.method == 'POST':
        form = RequestWithForm(request.POST)
        if form.is_valid():
            request_item = Requests.objects.get(id=pk)
            user = request_item.user
            start_date = request_item.start_date
            end_date = request_item.end_date
            Item.objects.filter(Q(start_date__range=(start_date, end_date))|Q(end_date__range=(start_date, end_date)),
                                added_by=user).update(shared_with=form.cleaned_data['share_with'])
            Requests.objects.get(id=pk).delete()
        return redirect('hello_world')
    else:
        request_item = Requests.objects.get(id=pk)
        user = request_item.user
        start_date = request_item.start_date
        end_date = request_item.end_date
        item = Item.objects.filter(Q(start_date__range=(start_date, end_date))|Q(end_date__range=(start_date, end_date)),
                                   added_by=user)
        form = RequestWithForm()
    return render(request, 'verify/request_info_list.html',
                  {'object': item,
                   'form': form})


def verifier_detail_view(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404('User does not exist')

    return render(request, 'verify/verifier_detail.html', context={'user': user})


def requester_detail_view(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404('User does not exist')

    return render(request, 'verify/requester_detail.html', context={'user': user})
