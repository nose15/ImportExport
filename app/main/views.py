from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import models, forms, routeManager
from django.conf import settings
from django.contrib.auth.models import User

# Create your views here.


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
            #routeManager.set_local_route(User.objects.get_by_natural_key("kierowca1"), models.Car.objects.get(registration_number="WE45812"), "Delivery")

            return HttpResponseRedirect("paczka/%s" % package.id)

        return render(response, "main/send.html", {"form": form})
    else:
        form = forms.CreateNewPackage()

    return render(response, "main/send.html", {"form": form})


def package_status_page(response):

    if response.method == "POST":
        form = forms.PassPackageID(response.POST)

        if form.is_valid():
            return HttpResponseRedirect("paczka/%s" % form.cleaned_data["package_id"])

    else:
        form = forms.PassPackageID()

    return render(response, "main/status.html", {"form": form})


def package_page(response, package_id):
    package_object = models.Package.objects.get(id=package_id)
    return render(response, "main/package.html", {"package": package_object})


def userpanel(request):
    user = request.user
    user_type = user.groups.first().name

    if user_type == 'Drivers':
        route_points = []
        route_type = None

        if user.driverdata.route_id is not None:
            route_points = list(models.Package.objects.filter(route_id=user.driverdata.route_id).order_by("route_order"))
            route_type = user.driverdata.route_id.route_type

            if request.method == "POST":
                if request.POST.get('submit_package'):
                    package_id = request.POST.get('submit_package')
                    package = models.Package.objects.get(id=package_id)
                    package.submit()
                    return HttpResponseRedirect("userpanel")

                elif request.POST.get('finish_route'):
                    packages = list(models.Package.objects.filter(route_id=user.driverdata.route_id))

                    for package in packages:
                        package.finish_route(package.origin_warehouse)

                    car = models.Car.objects.get(driver_id=user)
                    car.route_id = None
                    car.driver_id = None
                    car.save()
                    user.driverdata.route_id = None
                    user.driverdata.save()
                    return HttpResponseRedirect("userpanel")

        return render(
            request,
            "main/userpanel.html",
            {
                "user_type": user_type,
                "route_points": route_points,
                "route_type": route_type
            }
        )

    elif user_type == 'Warehouse Managers':
        warehouse = user.warehousemanagerdata.warehouse
        packages = list(models.Package.objects.filter(state='At warehouse', current_warehouse=warehouse))
        num_of_packages = len(packages)

        if request.method == "POST":
            if request.POST.get('assign_local_routes'):
                routeManager.assign_local_routes(user.warehousemanagerdata.warehouse)
            elif request.POST.get('assign_global_routes'):
                routeManager.assign_global_routes(user.warehousemanagerdata.warehouse)

        return render(
            request,
            "main/userpanel.html",
            {
                "user_type": user_type,
                "packages": packages,
                "num_of_packages": num_of_packages,
            }
        )
