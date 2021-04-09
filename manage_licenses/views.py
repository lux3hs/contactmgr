
import json

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse

from .models import License
from .services import (package_license_data, 
                      generate_license_key, 
                      read_key_file, 
                      add_new_license, 
                      get_license_table_header,
                      get_client_license_table_header,
                      delete_license_data,
                      )
                      
from manage_contacts.models import Contact, Organization
from manage_contacts.services import get_table_data



@login_required
def download_license_package(request, license_data, master_license_package=False):
    """ Download a product license if entitlements exist  """

    if license_data.check_allocated_licenses():
        
        license_data.subtract_license()
        data_package = package_license_data(license_data)
        key_name = generate_license_key(data_package)

        if key_name is not None:
            key_text = read_key_file(key_name)

            if master_license_package:
                m_key_name = generate_license_key(master_license_package)

                if m_key_name is not None:
                    key_field = "Key0=" + key_text

                    m_key_text = read_key_file(m_key_name)
                    m_key_field = "MKey=" + m_key_text

                    key_data = (master_license_package['master_header'] + "\r\n" +
                               master_license_package['entitlement_string'] + "\r\n" +"\r\n" +
                               m_key_field + "\r\n" +
                               key_field)

            else:
                key_field = "Key=" + key_text
                key_data = data_package['header_string'] + key_field

            response = HttpResponse(key_data, content_type="text/plain")
            response['Content-Disposition'] = 'attachment; filename="product-license.lic"'
            return response
            
    else: 
        messages.add_message(request, messages.INFO, 'Not enough licenses')
        response = HttpResponseRedirect(reverse('manage_contacts'))
        return response


@login_required
def delete_license_selection(request, query_string):
    """ Delete license data on user request """
    license_selection = json.loads(query_string)
    delete_check = delete_license_data(license_selection)
    if delete_check: 
        data = get_license_data(request)
        return data

    else:
        response = HttpResponse("error", content_type="text/plain")
        return response


@login_required
def get_license_data(request):
    """ Provide table data for populating licenses """
    license_data = License.objects.filter()
    table_header = get_license_table_header()
    table_data = get_table_data(table_header, license_data)

    return JsonResponse(table_data)

@login_required
def get_client_license_data(request):
    current_user = request.user
    user_id = current_user.id
    contact_data = Contact.objects.filter(user=user_id).get()
    org_id = contact_data.organization.id
    org_data = Organization.objects.filter(id=org_id).get()
    org_name = org_data.org_name

    license_data = License.objects.filter(org_name=org_name)
    table_header = get_client_license_table_header()
    table_data = get_table_data(table_header, license_data)

    return JsonResponse(table_data)



