from . import models
import googlemaps

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


def get_closest_package(origin_coords, packages):
    closest_package = None
    road_to_closest_package_duration = 9999999999

    for package in packages:
        package_coords = (package.origin_latitude, package.origin_longitude)

        duration = get_route(origin_coords, package_coords)['duration']

        if duration < road_to_closest_package_duration:
            closest_package = package
            road_to_closest_package_duration = duration

    return {'package': closest_package, 'duration': road_to_closest_package_duration}


def set_pickup_route(driver, car):
    route_packages = []

    driver_location = (driver.driverdata.location_latitude, driver.driverdata.location_longitude)
    warehouse = driver.driverdata.current_warehouse
    warehouse_coords = (warehouse.location_latitude, warehouse.location_longitude)
    packages = list(models.Package.objects.filter(origin_warehouse=warehouse))

    car_capacity = car.capacity
    car_filled = car.filled

    origin_coords = driver_location
    route_duration = 0
    comeback_route_duration = 0

    while route_duration < 7200 and car_filled < car_capacity:
        closest_package = get_closest_package(origin_coords, packages)

        packages.remove(closest_package['package'])
        route_packages.append(closest_package['package'])

        route_duration -= comeback_route_duration

        closest_package_coords = (closest_package['package'].origin_latitude, closest_package['package'].origin_longitude)
        comeback_route_duration = get_route(closest_package_coords, warehouse_coords)['duration']

        route_duration = route_duration + closest_package['duration'] + comeback_route_duration

        origin_package = route_packages[-1]
        origin_coords = (origin_package.origin_latitude, origin_package.origin_longitude)

    route = models.Route(duration=route_duration, type=models.Route.types[1])
    route.save()

    for route_package in route_packages:
        route_package.route_id = route
        route_package.car_id = car
        route_package.save()

    driver.driverdata.route_id = route
    car.driver_id = driver
    car.route_id = route
    car.filled = car_filled

    driver.driverdata.save()
    driver.save()
    car.save()




