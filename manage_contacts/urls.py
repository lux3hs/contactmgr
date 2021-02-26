from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_contacts, name='manage_contacts'),
    path('add', views.add_contact, name="add_contact")
]