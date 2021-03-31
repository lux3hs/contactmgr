from django.urls import path

from . import views

urlpatterns = [
    path('', views.manage_licenses, name="manage_licenses"),
    path('download-license-package', views.download_license_package, name='download_license_package'),
    # path('get-license-data', views.get_license_data, name='get_license_data'),
    # path('delete-license-selection/<str:query_string>/', views.delete_license_selection, name='delete_license_selection'),

]