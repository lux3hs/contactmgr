from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_contacts, name='manage_contacts'),
    path('admin-portal', views.admin_portal, name="admin_portal"),
    path('client-portal', views.client_portal, name="client_portal"),
    path('add-contact', views.add_contact, name="add_contact"),
    path('add-organization', views.add_organization, name="add_organization"),
    path('add-product', views.add_product, name="add_product"),
    # path('add-entitlement', views.add_entitlement, name="add_entitlement"),
    path('edit-org-data/<str:query_string>', views.edit_org_data, name="edit_org_data"),
    path('edit-contact-data/<str:query_string>', views.edit_contact_data, name="edit_contact_data"),
    path('edit-product-data/<str:query_string>', views.edit_product_data, name="edit_product_data"),
    path('edit-entitlement-data/<str:query_string>', views.edit_entitlement_data, name="edit_entitlement_data"),
    path('get-contact-data', views.get_contact_data, name="get_contact_data"),
    path('get-org-data', views.get_org_data, name='get_org_data'),
    path('get-product-data', views.get_product_data, name='get_product_data'),
    path('get-entitlement-data', views.get_entitlement_data, name='get_entitlement_data'),
    path('delete-contact-selection/<str:query_string>/', views.delete_contact_selection, name='delete_contact_selection'),
    path('delete-org-selection/<str:query_string>/', views.delete_org_selection, name='delete_org_selection'),
    path('delete-product-selection/<str:query_string>/', views.delete_product_selection, name='delete_product_selection'),
    path('delete-entitlement-selection/<str:query_string>/', views.delete_entitlement_selection, name='delete_entitlement_selection'),

]