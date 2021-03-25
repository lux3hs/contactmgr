from django.urls import path

from . import views

urlpatterns = [
    path('', views.manage_licenses, name='manage_licenses'),
    path('download-license-package', views.download_license_package, name='download_license_package'),
    path('get-entitlement-data', views.get_entitlement_data, name='get_entitlement_data'),
    path('get-license-data', views.get_license_data, name='get_license_data'),
    # path('generate-license-data', views.generate_license_data, name='generate_license_data'),
    path('delete-license-selection/<int:license_id>/', views.delete_license_selection, name='delete_license_selection'),
    # path('generate-license-selection/<int:license_id>/', views.generate_license_selection, name='generate_license_selection'),
    # path('generate-license-selection', views.generate_license_selection, name='generate_license_selection'),
    # path('download-license-package/<str:license_list>', views.download_license_package, name='download_license_package'),


]