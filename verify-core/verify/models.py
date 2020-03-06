from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Actions(models.Model):
    ADD_LIVING_EVENT = 'Added Living Event'
    ADD_WORK_EVENT = 'Added Work Event'
    ADD_EDUCATION_EVENT = 'Added Education Event'
    ADD_DOCUMENT_EVENT = 'Added Document'
    VERIFY_EVENT = 'Verified User Event'
    SHARE_EVENT = 'Shared Event'
    ACTION_TYPES = (
        (ADD_LIVING_EVENT, 'Living Event'),
        (ADD_WORK_EVENT, 'Work Event'),
        (ADD_EDUCATION_EVENT, 'Education Event'),
        (ADD_DOCUMENT_EVENT, 'DOCUMENT Event'),
        (VERIFY_EVENT, 'Verify event'),
        (SHARE_EVENT, 'Share Event'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=1, choices=ACTION_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()


class Businesses(models.Model):
    BUSINESS_TYPE = [
        ("ES", "Estate Agent"),
        ("WO", "Work Experience"),
    ]
    business_type = models.CharField(max_length=1,
                                     choices=BUSINESS_TYPE)
    business_name = models.CharField(max_length=50)

    def __str__(self):
        """String representing the living Item"""
        return self.business_name


def user_directory_path(instance, filename):
    return 'user_{0}/{1}/{2}'.format(instance.user,
                                     instance.document_type,
                                     filename)


class Document(models.Model):
    PASSPORT = 'Passport'
    DRIVING_LICENCE = 'Driving Licence'
    GAS_ELECTRIC_BILL = 'Gas or Electric Bill'
    EDUCATION_EVIDENCE = 'Education Evidence'
    DOCUMENT_TYPES = (
        (PASSPORT, 'Passport'),
        (DRIVING_LICENCE, 'Driving Licence'),
        (GAS_ELECTRIC_BILL, 'Gas or Electric Bill'),
        (EDUCATION_EVIDENCE, 'Education Evidence'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    document = models.FileField(upload_to=user_directory_path)
    shared_with = models.ForeignKey(
        Businesses,
        related_name='document_shared_with',
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    action = GenericRelation(Actions)

    def __str__(self):
        """String representing the living Item"""
        return self.document


class Item(models.Model):
    """Model for Living Item"""
    LIVING = 'living'
    WORK = 'work'
    EDUCATION = 'education'
    EVENT_TYPES = (
        (LIVING, 'living'),
        (WORK, 'work'),
        (EDUCATION, 'education'),
    )
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    start_date = models.DateTimeField(
        help_text="The start date"
    )
    end_date = models.DateTimeField(
        help_text="The end Date"
    )
    address = models.CharField(
        help_text="The address of where you lived",
        max_length=200
    )
    verifier = models.ForeignKey(
        Businesses,
        related_name='living_verifier',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_verified = models.BooleanField(
        default=False
    )
    verified_by = models.ForeignKey(
        Businesses,
        related_name='living_verified_by',
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    shared_with = models.ForeignKey(
        Businesses,
        related_name='living_shared_with',
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    linked_docs = models.ForeignKey(
        Document,
        related_name='living_linked_docs',
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    verified_hash = models.CharField(max_length=30)
    verified_unique_id = models.CharField(max_length=30)
    action = GenericRelation(Actions)

    def __str__(self):
        """String representing the living Item"""
        return self.address


class User(AbstractUser):
    is_requester = models.BooleanField(default=False)
    is_verifier = models.BooleanField(default=False)
    BUSINESS_TYPE = [
        ("ES", "Estate Agent"),
        ("WO", "Work Experience"),
    ]
    business_type = models.CharField(max_length=30,
                                     choices=BUSINESS_TYPE,
                                     null=True)
    business_name = models.CharField(max_length=50, null=True)
    unique_id = models.CharField(max_length=100)


class Profile(models.Model):
    """Extending user info"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_address = models.CharField(max_length=30, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Requests(models.Model):
    start_date = models.DateTimeField(
        help_text="The start date"
    )
    end_date = models.DateTimeField(
        help_text="The end Date"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='requests_user'
    )
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='requests_requester'
    )
