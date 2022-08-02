from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('package_send', views.package_send_page, name="package_send"),
    path('package_check_status', views.package_status_page, name="package_check_status"),
    path('paczka/<str:package_id>', views.package_page, name="package"),
    path('userpanel', views.userpanel, name="userpanel")
]