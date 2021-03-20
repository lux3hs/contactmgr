from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_contacts, name='manage_contacts'),
    path('add-contact', views.add_contact, name="add_contact"),
    path('admin-dash', views.admin_dash, name="admin_dash"),
    path('add-organization', views.add_organization, name="add_organization"),
    path('add-product', views.add_product, name="add_product"),
    path('add-entitlement', views.add_entitlement, name="add_entitlement"),
    path('get-contact-data', views.get_contact_data, name="get_contact_data"),

]