from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_contacts, name='manage_contacts'),
    path('add-contact', views.add_contact, name="add_contact"),
    path('edit-contact', views.edit_contact, name="edit_contact")

]