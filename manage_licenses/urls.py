from django.urls import path

from . import views

urlpatterns = [
    path('', views.manage_licenses, name='manage_licenses'),
    path('download-license', views.download_license, name='download_license'),
    path('get-entitlement-data', views.get_entitlement_data, name='get_entitlement_data'),
    path('get-license-data', views.get_license_data, name='get_license_data'),
    # path('generate-license-data', views.generate_license_data, name='generate_license_data'),
    path('delete-license-selection/<int:license_id>/', views.delete_license_selection, name='delete_license_selection'),


]