from django.urls import path
from . import views

# from manage_licenses.views import get_license_data, get_client_license_data, delete_license_selection

urlpatterns = [
    path('', views.manage_contacts, name='manage_contacts'),
    path('admin-portal', views.admin_portal, name="admin_portal"),
    # path('client-portal', views.client_portal, name="client_portal"),
    path('add-contact', views.add_contact, name="add_contact"),
    path('add-organization', views.add_organization, name="add_organization"),
    path('add-product', views.add_product, name="add_product"),
    path('edit-org-data/<str:query_string>', views.edit_org_data, name="edit_org_data"),
    path('edit-contact-data/<str:query_string>', views.edit_contact_data, name="edit_contact_data"),
    path('edit-product-data/<str:query_string>', views.edit_product_data, name="edit_product_data"),
    path('get-contact-data', views.get_contact_data, name="get_contact_data"),
    path('get-org-data', views.get_org_data, name='get_org_data'),
    path('get-product-data', views.get_product_data, name='get_product_data'),
    path('delete-contact-selection/<str:query_string>/', views.delete_contact_selection, name='delete_contact_selection'),
    path('delete-org-selection/<str:query_string>/', views.delete_org_selection, name='delete_org_selection'),
    path('delete-product-selection/<str:query_string>/', views.delete_product_selection, name='delete_product_selection'),

    # path('get-license-data', get_license_data, name='get_license_data'),
    # path('get-client-license-data', get_client_license_data, name='get_client_license_data'),
    # path('delete-license-selection/<str:query_string>/', delete_license_selection, name='delete_license_selection'),

]