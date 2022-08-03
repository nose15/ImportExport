from .. import models
from . import routeManager


def new_package(form):
    name = form.cleaned_data["package_name"]
    sender_email = form.cleaned_data["sender_email"]
    receiver_email = form.cleaned_data["receiver_email"]
    origin_latitude = form.cleaned_data["origin_latitude"]
    origin_longitude = form.cleaned_data["origin_longitude"]
    destination_latitude = form.cleaned_data["destination_latitude"]
    destination_longitude = form.cleaned_data["destination_longitude"]

    package = models.Package(
        name=name,
        sender_email=sender_email,
        receiver_email=receiver_email,
        origin_latitude=origin_latitude,
        origin_longitude=origin_longitude,
        destination_latitude=destination_latitude,
        destination_longitude=destination_longitude,
    )

    package.save()
    routeManager.assign_warehouses(package)

    return package


def package_submit(package_id):
    package = models.Package.objects.get(id=package_id)
    package.submit()


def finish_route(user):
    route_type = user.driverdata.route_id.route_type
    packages = list(models.Package.objects.filter(route_id=user.driverdata.route_id))

    destination_warehouse = packages[0].destination_warehouse

    if route_type == "InterWarehouse":
        for package in packages:
            package.finish_route(destination_warehouse)

        user.driverdata.current_warehouse = destination_warehouse
        user.driverdata.location_latitude = destination_warehouse.location_latitude
        user.driverdata.location_longitude = destination_warehouse.location_longitude
    else:
        for package in packages:
            package.finish_route(package.origin_warehouse)

    car = models.Car.objects.get(driver_id=user)
    car.route_id = None
    car.driver_id = None
    car.save()

    user.driverdata.route_id = None
    user.driverdata.save()


