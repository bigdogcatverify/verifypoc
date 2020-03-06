import datetime
from uuid import uuid4

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from .models import (User, Profile, Businesses, Document,
                     Item, Requests)


class EnterLivingForm(forms.Form):
    start_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        required=True,
        help_text="Enter the date you moved in",
    )
    end_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        required=True,
        help_text="Enter the date you moved out"
    )
    address = forms.CharField(
        required=True,
        help_text="Address of where you lived"
    )
    verifier = forms.ModelChoiceField(
        queryset=Businesses.objects.all().order_by('business_name')
    )

    def start_date_correct(self):
        data = self.cleaned_data['start_date']

        if data > datetime.date.today():
            raise ValidationError(_('Invalid date - in the future'))

        return data

    def end_date_correct(self, start_date_correct):
        data = self.cleaned_data['end_date']

        if data < start_date_correct:
            raise ValidationError(_('Invalid end date - before start date'))


class EnterWorkForm(forms.Form):
    start_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        required=True,
        help_text="Enter the date you moved in",
    )
    end_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        required=True,
        help_text="Enter the date you moved out"
    )
    work_place = forms.CharField(
        required=True,
        help_text="The place where you worked"
    )
    verifier = forms.ModelChoiceField(
        queryset=Businesses.objects.all().order_by('business_name')
    )

    def start_date_correct(self):
        data = self.cleaned_data['start_date']

        if data > datetime.date.today():
            raise ValidationError(_('Invalid date - in the future'))

        return data

    def end_date_correct(self, start_date_correct):
        data = self.cleaned_data['end_date']

        if data < start_date_correct:
            raise ValidationError(_('Invalid end date - before start date'))


class EnterEducationForm(forms.Form):
    start_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        required=True,
        help_text="Enter the date you started",
    )
    end_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        required=True,
        help_text="Enter the date you finished"
    )
    institution = forms.CharField(
        required=True,
        help_text="The place where you studied"
    )
    verifier = forms.ModelChoiceField(
        queryset=Businesses.objects.all().order_by('business_name')
    )

    def start_date_correct(self):
        data = self.cleaned_data['start_date']

        if data > datetime.date.today():
            raise ValidationError(_('Invalid date - in the future'))

        return data

    def end_date_correct(self, start_date_correct):
        data = self.cleaned_data['end_date']

        if data < start_date_correct:
            raise ValidationError(_('Invalid end date - before start date'))


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('location', 'birth_date')


class RequesterSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'email',)

    def save(self):
        user = super().save(commit=False)
        unique_id = str(uuid4()).replace('-', '')
        user.is_requester = True
        user.unique_id = unique_id
        user.save()
        return user


class VerifierSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'email',
                  'business_type', 'business_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        unique_id = str(uuid4()).replace('-', '')
        user.is_verifier = True
        user.unique_id = unique_id
        if commit:
            user.save()
        return user


class ShareWithForm(forms.Form):
    share_with = forms.ModelChoiceField(queryset=Businesses.objects.all())


class RequestWithForm(forms.Form):
    share_with = forms.ModelChoiceField(queryset=Businesses.objects.all())


class LinkWithForm(forms.Form):
    link_with = forms.ModelChoiceField(queryset=Item.objects.none())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(LinkWithForm, self).__init__(*args, **kwargs)
        self.fields['link_with'].queryset = Item.objects.filter(added_by=self.user)


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document_type', 'document',)


class RequestForm(forms.ModelForm):
    start_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        }))
    end_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker2'
        }))
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_requester=True))

    class Meta:
        model = Requests
        fields = ('user', 'start_date', 'end_date')

