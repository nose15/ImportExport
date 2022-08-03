from django.http import HttpResponseRedirect
from .. import models


def fetch_routes_data(user):
    route_points = []
    route_type = None

    if user.driverdata.route_id is not None:
        route_type = user.driverdata.route_id.route_type

        if route_type != "InterWarehouse":
            route_points = list(
                models.Package.objects.filter(route_id=user.driverdata.route_id).order_by("route_order"))

        else:
            package = models.Package.objects.filter(route_id=user.driverdata.route_id).first()
            route_points = [
                (package.destination_warehouse.location_latitude, package.destination_warehouse.location_longitude)]

        HttpResponseRedirect("userpanel")

    return {"route_points": route_points, "route_type": route_type}


def fetch_package_data(package_id):
    package = models.Package.objects.get(id=package_id)
    package_data = {
        "package": package,
        "name": package.name,
        "status": package.state,
        "sender_email": package.sender_email,
        "sender_location": (package.origin_latitude, package.origin_longitude),
        "receiver_email": package.receiver_email,
        "receiver_location": (package.destination_latitude, package.destination_longitude),
    }

    return package_data


def fetch_warehouse_data(warehouse):
    packages = list(models.Package.objects.filter(state='At warehouse', current_warehouse=warehouse))
    num_of_packages = len(packages)

    return {"packages": packages, "num_of_packages": num_of_packages}
