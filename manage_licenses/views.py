import datetime
import os.path

import json


from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from json import dumps

from django.contrib.auth.decorators import login_required
from django.conf import settings

from manage_contacts.models import Contact, Product, Entitlement, Organization
from .models import License
from .forms import ChoiceForm, SearchForm, NewLicenseForm, SearchChoiceForm
from .services import *

base_dir = str(settings.BASE_DIR)

# Create your views here.

@login_required
def manage_licenses(request):
    """ Render manage-licenses html page """
    current_user = request.user
    user_id = current_user.id
    contact_data = Contact.objects.filter(user=user_id).get()
    org_id = contact_data.organization.id

    
    product_entitlements = Entitlement.objects.filter(organization=org_id)
    product_choices = []
    for entitlement in product_entitlements:
        product_choices.append((entitlement.product.product_name, entitlement.product.product_name))

    
    
    new_license_form = NewLicenseForm(product_choices=product_choices)


    if request.POST.get("save-license"):
        user_query = request.POST
        product_choice = user_query.get('product_choice')

        entitlement_product = Product.objects.filter(product_name=product_choice).get()
        product_id = entitlement_product.id
        entitlement_data = product_entitlements.filter(product=product_id).get()

        if entitlement_data.check_allocated_licenses():  
            delete_check = create_license(current_user, user_query)

            if delete_check:
                entitlement_data.subtract_license()

                messages.add_message(request, messages.INFO, 'new license created')
                return HttpResponseRedirect(request.path_info)

        else:
            messages.add_message(request, messages.INFO, 'no entitlements')
            return HttpResponseRedirect(request.path_info)

    if request.POST.get ("download-license-button"):
        license_selection = request.POST.getlist("check-box")
        
        product_entitlements = Entitlement.objects.filter(organization=org_id)

        license_check = check_license_data(license_selection)

        if license_check:
            
            package_data = package_license_data(license_selection)
            key_data = generate_license_key(package_data)

            for license_id in license_selection:
                delete_license(license_id)

            return download_license_package(request, key_data)

        else:
            context = {'new_license_form':new_license_form}
            messages.success(request, 'No licenses selected')
            
            return render(request, "manage_licenses/manage-licenses.html", context)

    context = {'new_license_form':new_license_form}

    return render(request, "manage_licenses/manage-licenses.html", context)



def download_license_package(request, data):
    """ Download a generated license """
    response = HttpResponse(data, content_type="text/plain")
    response['Content-Disposition'] = 'attachment; filename="product-license.lic"'
    return response


def delete_license_selection(request, license_query):
    license_data = License.objects.filter(id=license_id).get()
    entitlement_id = license_data.entitlement_id
    entitlement_data = Entitlement.objects.filter(id=entitlement_id).get()
    delete_check = delete_license(license_id)

    if delete_check: 
        entitlement_data.add_license()
        data = get_license_data(request)
        return data

    else:
        response = HttpResponse("error", content_type="text/plain")
        return response


def get_entitlement_data(request):
    current_user = request.user
    user_id = current_user.id
    contact_data = Contact.objects.filter(user=user_id).get()
    org_id = contact_data.organization.id
    entitlement_data = Entitlement.objects.filter(organization=org_id)

    table_header = get_entitlement_header()
    table_data = get_table_data(table_header, entitlement_data)
    return JsonResponse(table_data)


def get_license_data(request):
    current_user = request.user
    user_id = current_user.id
    contact_data = Contact.objects.filter(user=user_id).get()
    org_id = contact_data.organization.id
    license_data = License.objects.filter(org_id=org_id)
    table_header = get_license_header()
    table_data = get_table_data(table_header, license_data)
    return JsonResponse(table_data)


