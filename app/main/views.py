from django.shortcuts import render
from django.http import HttpResponseRedirect

from . import models, forms, routeManager

import packageManager
import dataFetcher


def home_page(response):
    return render(response, "main/home.html", {})


def package_send_page(response):
    if response.method == "POST":
        form = forms.CreateNewPackage(response.POST)

        if form.is_valid():
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

            return HttpResponseRedirect("paczka/%s" % package.id)

        return render(response, "main/send.html", {"form": form})
    else:
        form = forms.CreateNewPackage()

    return render(response, "main/send.html", {"form": form})


def package_status_page(response, package_id):
    package_data = dataFetcher.fetch_package_data(package_id)
    if response.method == "POST":
        form = forms.PassPackageID(response.POST)

        if form.is_valid():
            return HttpResponseRedirect("paczka/%s" % form.cleaned_data["package_id"])

    else:
        form = forms.PassPackageID()

    return render(response, "main/status.html", {"form": form})


def package_page(response, package_id):
    package_data = dataFetcher.fetch_package_data(package_id)

    # view here

    return render(response, "main/package.html", {})


def userpanel(request):
    user = request.user
    user_type = user.groups.first().name

    if user_type == 'Drivers':
        driver_routes_data = dataFetcher.fetch_routes_data(user, request)
        # driver_routes_data = {'route_points': <list of Package objects>, 'route_type': <models.Route.route_type>}

        # view here

        if request.method == "POST":
            # {'submit_package': <package id>}
            if request.POST.get('submit_package'):
                package_id = request.POST.get('submit_package')
                packageManager.package_submit(package_id)
            elif request.POST.get('finish_route'):
                packageManager.finish_route(user)

            return HttpResponseRedirect("userpanel")

        return render(
            request,
            "main/userpanel.html",
            {
                "user_type": user_type,
                "route_points": driver_routes_data['route_points'],
                "route_type": driver_routes_data['route_type']
            }
        )

    elif user_type == 'Warehouse Managers':
        warehouse = user.warehousemanagerdata.warehouse
        warehouse_data = dataFetcher.fetch_warehouse_data(warehouse)
        # warehouse_data = {'packages': <list of Package objects>, 'num_of_packages': <int>}

        # view here

        if request.method == "POST":
            if request.POST.get('assign_local_routes'):
                routeManager.assign_local_routes(warehouse)
            elif request.POST.get('assign_global_routes'):
                routeManager.assign_global_routes(warehouse)

        return render(
            request,
            "main/userpanel.html",
            {
                "user_type": user_type,
                "packages": warehouse_data['packages'],
                "num_of_packages": warehouse_data['num_of_packages'],
            }
        )


