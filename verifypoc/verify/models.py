from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


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
    verifier = models.CharField(
        help_text="The person who can verify this",
        max_length=200
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
    verifier = models.CharField(
        help_text="The person who can verify this",
        max_length=200
    )

    def __str__(self):
        """String representing the living Item"""
        return self.work_place


class User(AbstractUser):
    is_requester = models.BooleanField(default=False)
    is_verifier = models.BooleanField(default=False)


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