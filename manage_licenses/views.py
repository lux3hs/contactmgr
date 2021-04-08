
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from manage_contacts.models import Product, Contact, Entitlement
from .services import package_license_data, generate_license_key, read_key_file, add_new_license
# from manage_licenses.services import add_new_license

@login_required
def download_license_package(request, user_query, entitlement_choice, master_license_package=False):
    """ Download a product license if entitlements exist  """
    current_user = request.user
    user_id = current_user.id
    contact_data = Contact.objects.filter(user=user_id).get()

    entitlement_data = entitlement_choice
    if entitlement_data.check_allocated_licenses():

        new_license = add_new_license(contact_data, entitlement_data, user_query)
        license_data = new_license
        
        entitlement_data.subtract_license()
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




# @login_required
# def delete_license_selection(request, query_string):
#     """ Delete license data on user request """
#     license_selection = json.loads(query_string)
#     delete_check = delete_license_data(license_selection)
#     if delete_check: 
#         data = get_license_data(request)
#         return data

#     else:
#         response = HttpResponse("error", content_type="text/plain")
#         return response


# @login_required
# def get_license_data(request):
#     """ Provide table data for populating licenses """
#     current_user = request.user
#     user_id = current_user.id
#     contact_data = Contact.objects.filter(user=user_id).get()
#     org_id = contact_data.organization.id
#     license_data = License.objects.filter(org_id=org_id)
#     table_header = get_license_header()
#     table_data = get_table_data(table_header, license_data)
#     return JsonResponse(table_data)


