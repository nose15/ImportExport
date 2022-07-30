from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import models, forms

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

