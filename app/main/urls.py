from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('wysylanie_paczki', views.package_send_page, name="package_send"),
    path('paczka/', views.package_status_page, name="search_for_package"),
    path('paczka/<str:package_id>', views.package_status_page, name="package"),
    path('userpanel', views.userpanel, name="userpanel")
]