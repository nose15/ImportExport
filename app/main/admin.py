from django.contrib import admin
from .models import Package, PackageStateTransitions

# Register your models here.
admin.site.register(Package)
admin.site.register(PackageStateTransitions)
