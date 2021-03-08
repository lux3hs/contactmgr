from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_licenses, name='generate_licenses'),
    path('ml-new', views.ml_new, name='ml_new'),


    path('return-list', views.ml_return_list, name='return_list'),
    path('product-names', views.productNameShortcut, name='productNameShortcut'),
    path('load-record', views.ml_load_record, name='load_record'),
    path('save-license', views.save_license_to_db, name='save_license_to_db'),
    path('save-status', views.save_license_active_status_to_db, name='save_license_active_status_to_db'),
    path('download-master-license', views.download_master_license_file, name='download_master_license_file'),
    path('generate-license', views.generate_single_license, name='generate_single_license'),
    path('download-single-license', views.download_single_license_file, name='download_single_license_file'),
    path('new-station-name', views.newScenarioStationLicenseName, name='newScenarioStationLicenseName'),

]