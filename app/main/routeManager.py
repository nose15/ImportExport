from . import models
import googlemaps
import math
from django.contrib.auth.models import User

API_key = 'AIzaSyDHFU-OcOH-r_wsQgpbKEY5Hphb8-WV7JI'
gmaps = googlemaps.Client(key=API_key)

warehouses = models.Warehouse.objects.all()


def assign_warehouses(package):
    sender_coords = (package.origin_latitude, package.origin_longitude)
    receiver_coords = (package.destination_latitude, package.destination_longitude)

    closest_warehouse_to_sender = None
    closest_warehouse_to_sender_distance = 9999999999

    closest_warehouse_to_receiver = None
    closest_warehouse_to_receiver_distance = 9999999999

    for warehouse in warehouses:
        warehouse_coords = (warehouse.location_latitude, warehouse.location_longitude)

        distance_to_sender = gmaps.distance_matrix(
            warehouse_coords,
            sender_coords,
            mode='driving'
        )["rows"][0]["elements"][0]["distance"]["value"]

        distance_to_receiver = gmaps.distance_matrix(
            warehouse_coords,
            receiver_coords,
            mode='driving'
        )["rows"][0]["elements"][0]["distance"]["value"]

        if distance_to_sender < closest_warehouse_to_sender_distance:
            closest_warehouse_to_sender = warehouse
            closest_warehouse_to_sender_distance = distance_to_sender

        if distance_to_receiver < closest_warehouse_to_receiver_distance:
            closest_warehouse_to_receiver = warehouse
            closest_warehouse_to_receiver_distance = distance_to_receiver

    package.origin_warehouse = closest_warehouse_to_sender
    package.destination_warehouse = closest_warehouse_to_receiver

    package.save()


def get_route(origin_coords, destination_coords):
    route = gmaps.distance_matrix(
        origin_coords,
        destination_coords,
        mode='driving'
    )["rows"][0]["elements"][0]

    distance = route["distance"]["value"]
    duration = route["duration"]["value"]

    return {'distance': distance, 'duration': duration}


def get_closest_package(origin_coords, packages, route_type):
    closest_package = None
    road_to_closest_package_duration = 9999999999

    for package in packages:
        package_coords = (package.origin_latitude, package.origin_longitude) \
            if route_type == "PickUp" else (package.destination_latitude, package.destination_longitude)

        duration = get_route(origin_coords, package_coords)['duration']

        if duration < road_to_closest_package_duration:
            closest_package = package
            road_to_closest_package_duration = duration

    return {'package': closest_package, 'duration': road_to_closest_package_duration}


def set_local_route(driver, car, route_type):
    route_packages = []
    packages = []

    driver_location = (driver.driverdata.location_latitude, driver.driverdata.location_longitude)
    warehouse = driver.driverdata.current_warehouse
    warehouse_coords = (warehouse.location_latitude, warehouse.location_longitude)

    if route_type == "PickUp":
        packages = list(models.Package.objects.filter(
            origin_warehouse=warehouse,
            state="Registered"
        ))

    elif route_type == "Delivery":
        packages = list(models.Package.objects.filter(
            destination_warehouse=warehouse,
            current_warehouse=warehouse,
            state="At warehouse"
        ))

    car_capacity = car.capacity
    car_filled = 0

    origin_coords = driver_location
    route_duration = 0
    comeback_route_duration = 0

    package_route_order_index = 0

    while route_duration < 7200 and car_filled < car_capacity and len(packages) > 0:
        closest_package = get_closest_package(origin_coords, packages, route_type)

        closest_package['package'].route_order = package_route_order_index

        packages.remove(closest_package['package'])
        route_packages.append(closest_package['package'])

        route_duration -= comeback_route_duration

        if route_type == "PickUp":
            closest_package_coords = (
                closest_package['package'].origin_latitude,
                closest_package['package'].origin_longitude
            )

        elif route_type == "Delivery":
            closest_package_coords = (
                closest_package['package'].destination_latitude,
                closest_package['package'].destination_longitude
            )

            closest_package['package'].state = 'En route'

        closest_package['package'].save()

        comeback_route_duration = get_route(closest_package_coords, warehouse_coords)['duration']
        route_duration = route_duration + closest_package['duration'] + comeback_route_duration

        car_filled += 1
        package_route_order_index += 1

        origin_coords = closest_package_coords

    route = models.Route(duration=route_duration, route_type=route_type)
    route.save()

    for route_package in route_packages:
        route_package.route_id = route
        route_package.car_id = car if route_type == "PickUp" else None
        route_package.save()

    driver.driverdata.route_id = route
    car.driver_id = driver
    car.route_id = route
    car.filled = car_filled if route_type == "Delivery" else 0

    driver.driverdata.save()
    driver.save()
    car.save()


def set_interwarehouse_route(origin_warehouse, destination_warehouse):

    origin_warehouse_coords = (origin_warehouse.location_latitude, origin_warehouse.location_longitude)
    destination_warehouse_coords = (destination_warehouse.location_latitude, destination_warehouse.location_longitude)

    duration = get_route(origin_warehouse_coords, destination_warehouse_coords)['duration']

    route = models.Route(route_type="InterWarehouse", duration=duration)
    route.save()

    packages = list(models.Package.objects.filter(
        current_warehouse=origin_warehouse,
        origin_warehouse=origin_warehouse,
        destination_warehouse=destination_warehouse,
        route_id=None
    ))

    quantity_of_packages = len(packages)

    if quantity_of_packages > 0:
        cars_needed = math.ceil(quantity_of_packages / 200)
        packages_per_car = math.ceil(quantity_of_packages / cars_needed)

        package_index = 0

        for i in range(cars_needed):
            car = models.Car.objects.filter(current_warehouse=origin_warehouse, busy=False).first()
            car.save()

            for j in range(packages_per_car):
                try:
                    package = packages[package_index]
                    package.car_id = car
                    package.route_id = route
                    package.state = "En Route"

                    package_index += 1
                    car.filled += 1

                    package.save()

                    print(package.route_id)
                except IndexError:
                    break

            driverdata = models.DriverData.objects.filter(current_warehouse=origin_warehouse, route_id=None).first()

            driverdata.route_id = route

            car.driver_id = driverdata.user
            car.route_id = route
            car.save()
            driverdata.save()


def assign_local_routes(warehouse):
    packages_to_pickup = list(models.Package.objects.filter(state='Registered', origin_warehouse=warehouse, route_id=None))
    packages_to_deliver = list(models.Package.objects.filter(state='At Warehouse', current_warehouse=warehouse, destination_warehouse=warehouse))

    drivers = list(models.DriverData.objects.filter(route_id=None, current_warehouse=warehouse))
    cars = list(models.Car.objects.filter(route_id=None, driver_id=None, filled=0, current_warehouse=warehouse))

    while len(packages_to_pickup) != 0:
        set_local_route(drivers[0].user, cars[0], 'PickUp')
        drivers.remove(drivers[0])
        cars.remove(cars[0])
        packages_to_pickup = list(
            models.Package.objects.filter(state='Registered', origin_warehouse=warehouse, route_id=None))

    while len(packages_to_deliver) != 0:
        set_local_route(drivers[0], cars[0], 'Delivery')
        drivers.remove(drivers[0])
        cars.remove(cars[0])
        packages_to_deliver = list(models.Package.objects.filter(state='At Warehouse', current_warehouse=warehouse,
                                                                 destination_warehouse=warehouse, route_id=None))


def assign_global_routes(origin_warehouse):
    warehouses_global = list(models.Warehouse.objects.exclude(name=origin_warehouse.name))

    for warehouse in warehouses_global:
        set_interwarehouse_route(origin_warehouse, warehouse)
