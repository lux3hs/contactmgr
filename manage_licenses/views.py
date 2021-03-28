import datetime
import os.path

import json


from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from django.contrib.auth.decorators import login_required
from django.conf import settings

from manage_contacts.models import Contact, Product, Entitlement
from .models import License
from .forms import NewLicenseForm

#Specify method imports
from .services import *

base_dir = str(settings.BASE_DIR)


@login_required
def client_portal(request):
    current_user = request.user
    user_id = current_user.id
    contact_data = Contact.objects.filter(user=user_id).get()
    context = {'contact_data':contact_data}
    return render(request, "manage_licenses/client-portal.html", context)


@login_required
def manage_licenses(request):
    """ Render manage-licenses html page """
    print("hello")
    current_user = request.user
    user_id = current_user.id
    contact_data = Contact.objects.filter(user=user_id).get()
    org_id = contact_data.organization.id
    product_entitlements = Entitlement.objects.filter(organization=org_id)
    product_choices = []

    for entitlement in product_entitlements:
        product_choices.append((entitlement.product.product_name, entitlement.product.product_name))

    if request.POST.get("save-license"):
        new_license_form = NewLicenseForm(request.POST, product_choices=product_choices)

        if new_license_form.is_valid():

            user_query = request.POST
            product_choice = user_query.get('product_name')

            entitlement_product = Product.objects.filter(product_name=product_choice).get()
            product_id = entitlement_product.id
            entitlement_data = product_entitlements.filter(product=product_id).get()

            if entitlement_data.check_allocated_licenses(): 
                new_license = create_license(current_user, user_query)

                if new_license:
                    entitlement_data.subtract_license()

                    data_package = package_license_data(new_license.id)
                    key_name = generate_license_key(data_package)


                    if key_name is not None:
                        key_data = read_key_file(key_name)
                        return download_license_package(request, key_data)





    #                 messages.add_message(request, messages.INFO, 'new license created')
    #                 return HttpResponseRedirect(request.path_info)

    #         else:
    #             messages.add_message(request, messages.INFO, 'no entitlements')
    #             return HttpResponseRedirect(request.path_info)

    else:
        new_license_form = NewLicenseForm(product_choices=product_choices)


    # if request.POST.get ("download-license-button"):
    #     license_selection = request.POST.getlist("check-box")
    #     license_check = check_license_data(license_selection)

    #     if license_check:
            
            
            
        #     data_package = package_license_data(license_selection)
        #     key_name = generate_license_key(data_package)
            
        #     if key_name is not None:
        #         for license_id in license_selection:
        #             product_license = License.objects.filter(id=license_id)
        #             product_license.delete()
                
        #         key_data = read_key_file(key_name)
        #         return download_license_package(request, key_data)

        #     else:
        #         messages.success(request, 'package creation failed')
        #         return HttpResponseRedirect(request.path_info)

        # else:
        #     messages.success(request, 'no licenses selected')
        #     return HttpResponseRedirect(request.path_info)

    context = {'new_license_form':new_license_form}
   
   
    return render(request, "manage_licenses/manage-licenses.html", context)
    
    # response = HttpResponse("error", content_type="text/plain")
    # return response

@login_required
def download_license_package(request, data):
    """ Download a generated license """
    response = HttpResponse(data, content_type="text/plain")
    response['Content-Disposition'] = 'attachment; filename="product-license.lic"'
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
    current_user = request.user
    user_id = current_user.id
    contact_data = Contact.objects.filter(user=user_id).get()
    org_id = contact_data.organization.id
    license_data = License.objects.filter(org_id=org_id)
    table_header = get_license_header()
    table_data = get_table_data(table_header, license_data)
    return JsonResponse(table_data)


@login_required
def get_entitlement_data(request):
    """ Provide entitlement data for populating tables """
    current_user = request.user
    user_id = current_user.id
    contact_data = Contact.objects.filter(user=user_id).get()
    org_id = contact_data.organization.id
    entitlement_data = Entitlement.objects.filter(organization=org_id)
    table_header = get_entitlement_header()
    table_data = get_table_data(table_header, entitlement_data)
    return JsonResponse(table_data)
