from django.urls import path

from . import views

urlpatterns = [
    path('', views.manage_licenses, name='manage_licenses'),
    path('download-license', views.download_license, name='download_license'),

]