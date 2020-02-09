from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# TODO add for education event


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


class LivingItem(models.Model):
    """Model for Living Item"""
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

    def __str__(self):
        """String representing the living Item"""
        return self.address


class WorkItem(models.Model):
    """Model for Living Item"""
    start_date = models.DateTimeField(
        help_text="The start date"
    )
    end_date = models.DateTimeField(
        help_text="The end Date"
    )
    work_place = models.CharField(
        help_text="The place where you worked",
        max_length=200
    )
    verifier = models.ForeignKey(
        Businesses,
        related_name='work_verifier',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    is_verified = models.BooleanField(
        default=False
    )
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    shared_with = models.ForeignKey(
        Businesses,
        related_name='work_shared_with',
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        """String representing the living Item"""
        return self.work_place


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
