from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import uuid

registered = 'Registered'
en_route = 'En Route'
delivered = 'Delivered'
at_warehouse = 'At warehouse'
delivery_confirmed = 'Delivery Confirmed'
states = [
    (registered, 'Registered'),
    (en_route, 'En Route'),
    (delivered, 'Delivered'),
    (at_warehouse, 'At warehouse'),
    (delivery_confirmed, 'Delivery Confirmed')
]


class Warehouse(models.Model):
    name = models.CharField(max_length=60, primary_key=True)

    location_latitude = models.FloatField()
    location_longitude = models.FloatField()


class Route(models.Model):
    types = [
        ('InterWarehouse', 'InterWarehouse'),
        ('PickUp', 'PickUp'),
        ('Delivery', 'Delivery'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    duration = models.FloatField(default=0)
    route_type = models.CharField(choices=types, max_length=60)


class WarehouseManagerData(models.Model):
    user = models.OneToOneField(User, blank=True, on_delete=models.CASCADE)

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )


class DriverData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    location_latitude = models.FloatField()
    location_longitude = models.FloatField()

    current_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )

    route_id = models.ForeignKey(
        Route,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )


class Car(models.Model):
    registration_number = models.CharField(max_length=7, primary_key=True)
    capacity = models.IntegerField()
    filled = models.IntegerField()

    type = models.CharField(max_length=10, choices=[('van', 'van'), ('truck', 'truck')], default='van')

    current_warehouse = models.ForeignKey(
        Warehouse,
        related_name="Current_Car_W",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None
    )

    driver_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'groups__name': "Drivers"},
        related_name="Drivers",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None
    )

    route_id = models.ForeignKey(
        Route,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )


class Package(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60)
    state = models.CharField(
        max_length=60,
        choices=states,
        default=registered
    )

    sender_email = models.EmailField()
    receiver_email = models.EmailField()

    origin_latitude = models.FloatField()
    origin_longitude = models.FloatField()

    destination_latitude = models.FloatField()
    destination_longitude = models.FloatField()

    origin_warehouse = models.ForeignKey(
        Warehouse,
        related_name="Origin_W",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None
    )

    destination_warehouse = models.ForeignKey(
        Warehouse,
        related_name="Destination_W",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None
    )

    current_warehouse = models.ForeignKey(
        Warehouse,
        related_name="Current_W",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None
    )

    route_id = models.ForeignKey(
        Route,
        related_name="Routes",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None
    )

    car_id = models.ForeignKey(
        Car,
        related_name="Cars",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None
    )

    route_order = models.IntegerField(null=True, blank=True, default=None)

    def submit(self):
        if self.route_id.route_type == "PickUp":
            self.state = en_route
            self.car_id.filled += 1
        else:
            self.state = delivered
            self.car_id.filled -= 1

        self.car_id.save()
        self.save()

    def finish_route(self, warehouse):
        if self.route_id.route_type == "PickUp" or self.route_id.route_type == "InterWarehouse":
            if self.state == "En Route":
                self.current_warehouse = warehouse
                self.state = at_warehouse
                self.car_id.filled -= 1
        else:
            if self.state == "Delivered":
                self.current_warehouse = None

        self.car_id.save()

        self.route_id = None
        self.car_id = None
        self.route_order = None

        self.save()


class PackageStateTransitions(models.Model):
    package_id = models.ForeignKey(Package, related_name="Packages", on_delete=models.CASCADE)
    state = models.CharField(
        max_length=60,
        choices=states,
        default=registered
    )
    time = models.DateTimeField()


