from django.urls import path

from . import views

urlpatterns = [
    path('', views.manage_licenses, name='manage_licenses'),
    path('download-license', views.download_license, name='download_license'),
    path('get-entitlement-data', views.get_entitlement_data, name='get_entitlement_data'),
    path('get-license-data', views.get_license_data, name='get_license_data'),


]