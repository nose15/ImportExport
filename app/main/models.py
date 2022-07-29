from django.db import models
from django.conf import settings
import uuid

registered = 'RE'
en_route = 'ER'
delivered = 'DE'
at_warehouse = 'AW'
states = [
    (registered, 'Registered'),
    (en_route, 'En Route'),
    (delivered, 'Delivered'),
    (at_warehouse, 'At warehouse'),
]


class Warehouse(models.Model):
    name = models.CharField(max_length=60, primary_key=True)

    location_latitude = models.FloatField()
    location_longitude = models.FloatField()


class Route(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    origin_latitude = models.FloatField()
    origin_longitude = models.FloatField()

    destination_latitude = models.FloatField()
    destination_longitude = models.FloatField()

    interwarehouse = models.BooleanField()

    state = models.CharField(
        max_length=64
    )

    length = models.FloatField(default=0)


class Car(models.Model):
    registration_number = models.CharField(max_length=7, primary_key=True)
    capacity = models.IntegerField()
    filled = models.IntegerField()

    origin_warehouse = models.ForeignKey(
        Warehouse,
        related_name="Current_Car_W",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )

    driver_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'groups__name': "Drivers"},
        related_name="Drivers",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )

    route_id = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )


class Package(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60)
    state = models.CharField(
        max_length=2,
        choices=states,
        default=registered
    )

    origin_latitude = models.FloatField()
    origin_longitude = models.FloatField()

    destination_latitude = models.FloatField()
    destination_longitude = models.FloatField()

    origin_warehouse = models.ForeignKey(
        Warehouse,
        related_name="Origin_W",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )

    destination_warehouse = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="Destination_W",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )

    current_warehouse = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="Current_W",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )

    sender_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'groups__name': "Customers"},
        related_name="Senders",
        on_delete=models.CASCADE,
        null=True,
        default=None
    )

    reciever_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'groups__name': "Customers"},
        related_name="Recievers",
        on_delete=models.CASCADE,
        null=True,
        default=None
    )

    route_id = models.ForeignKey(
        Route,
        related_name="Routes",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )

    car_id = models.ForeignKey(
        Car,
        related_name="Cars",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )


class PackageStateTransitions(models.Model):
    package_id = models.ForeignKey(Package, related_name="Packages", on_delete=models.CASCADE)
    state = models.CharField(
        max_length=2,
        choices=states,
        default=registered
    )
    time = models.DateTimeField()


