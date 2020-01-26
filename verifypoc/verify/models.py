from django.db import models
from django.urls import reverse


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
