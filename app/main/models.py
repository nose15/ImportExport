from django.db import models
from django.conf import settings
import uuid

registered = 'RE'
in_preparation = 'PR'
on_way = 'OW'
delivered = 'DE'
suspended = 'SU'
states = [
    (registered, 'Registered'),
    (in_preparation, 'In Preparation'),
    (on_way, 'On way'),
    (delivered, 'Delivered'),
    (suspended, 'Suspended'),
]


class Package(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60)
    state = models.CharField(
        max_length=2,
        choices=states,
        default=registered
    )

    customer_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'groups__name': "Customers"},
        related_name="Customers", on_delete=models.CASCADE
    )

    driver_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'groups__name': "Drivers"},
        related_name="Drivers", on_delete=models.CASCADE
    )


class PackageStateTransitions(models.Model):
    package_id = models.ForeignKey(Package, related_name="Packages", on_delete=models.CASCADE)
    state = models.CharField(
        max_length=2,
        choices=states,
        default=registered
    )
    time = models.DateTimeField()
