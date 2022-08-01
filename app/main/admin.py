from django.contrib import admin
from .models import Package, PackageStateTransitions, Route, Car, Warehouse, DriverData

# Register your models here.
admin.site.register(Package)
admin.site.register(PackageStateTransitions)
admin.site.register(Route)
admin.site.register(Car)
admin.site.register(Warehouse)
admin.site.register(DriverData)