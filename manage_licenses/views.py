
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from manage_contacts.models import Product
from .services import package_license_data, generate_license_key, read_key_file

@login_required
def download_license_package(request, product_choice, product_entitlements, master_license_package=False):
    """ Download a product license if entitlements exist  """
    entitlement_product = Product.objects.filter(product_name=product_choice).get()
    product_id = entitlement_product.id
    entitlement_data = product_entitlements.filter(product=product_id).get()
    if entitlement_data.check_allocated_licenses():
        
        entitlement_data.subtract_license()
        data_package = package_license_data(entitlement_data)
        key_name = generate_license_key(data_package)

        if key_name is not None:
            key_text = read_key_file(key_name)
            # key_field = "Key=" + key_text

            if master_license_package:
                m_key_name = generate_license_key(master_license_package)
                if m_key_name is not None:

                    # key_text = read_key_file(key_name)
                    key_field = "Key0=" + key_text

                    m_key_text = read_key_file(m_key_name)
                    m_key_field = "MKey=" + m_key_text


                    key_data = (master_license_package['master_header'] + "\r\n" +
                               master_license_package['entitlement_string'] + "\r\n" +"\r\n" +
                               m_key_field + "\r\n" + 
                               key_field)


            else:
                # key_text = read_key_file(key_name)
                key_field = "Key=" + key_text
                key_data = data_package['header_string'] + key_field

            entitlement_data.gen_license_image()

            

    else: 
        messages.add_message(request, messages.INFO, 'Not enough licenses')
        response = HttpResponseRedirect(reverse('manage_contacts'))
        return response

    response = HttpResponse(key_data, content_type="text/plain")
    response['Content-Disposition'] = 'attachment; filename="product-license.lic"'
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


