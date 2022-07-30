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

