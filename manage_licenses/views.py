import datetime
import os.path

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
    #Get current user info
    current_user = request.user
    user_email = current_user.email
    user_id = current_user.id

    contact_data = Contact.objects.filter(user=user_id).get()
    user_role = contact_data.role
    user_org = contact_data.organization
    org_id = contact_data.organization.id
    org_name = user_org.org_name

    product_entitlements = Entitlement.objects.filter(organization=org_id)


    license_header = get_license_header()
    license_choice_list = get_choice_list(license_header)
    license_search_form =  SearchChoiceForm(auto_id='license_search_form_%s', choice_list=license_choice_list)

    entitlement_header = get_entitlement_header()
    entitlement_choice_list = get_choice_list(entitlement_header)
    entitlement_search_form =  SearchChoiceForm(auto_id='entitlement_search_form_%s', choice_list=entitlement_choice_list)

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
            new_license = create_license(current_user, user_query)
            messages.add_message(request, messages.INFO, 'New license created')
            return HttpResponseRedirect(request.path_info)

        else:
            messages.add_message(request, messages.INFO, 'Not enough product entitlements')
            return HttpResponseRedirect(request.path_info)
    
    if request.POST.get("generate_license_selection"):
        user_selection = request.POST.getlist("check-box")
        
        if len(user_selection) > 0:
            license_array = generate_license_array(current_user, user_selection)

            if license_array["Success"]:
                new_license = download_license(request)
                return new_license

            else:
                response = HttpResponse(license_array["Message"], content_type="text/plain")
                return response

        else:
            response = HttpResponse("No licenses selected", content_type="text/plain")
            return response
    
    #Render variables in html
    context = {'user_email': user_email,
                'user_role': user_role,
                'user_org':org_name,
                'license_search_form':license_search_form,
                'new_license_form':new_license_form,
                'entitlement_search_form':entitlement_search_form,
                }

    return render(request, "manage_licenses/manage-licenses.html", context)


def download_license(request):
#     """ Download a generated license """
    license_file = base_dir + "/bin/Product-License.lic"
    if os.path.isfile(license_file):
        print("hello")
        f = open(license_file, "r")
        license_data = f.read()
        license_data = license_data.replace("\n", "\r\n")
        os.remove(license_file)
        response = HttpResponse(license_data, content_type="text/plain")
        response['Content-Disposition'] = 'attachment; filename="product-license.lic"'
        return response

    else:
        response = HttpResponse("No file exists", content_type="text/plain")
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


def delete_license_selection(request, license_id):
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

        




    # print(check_entitlements(product, org))

    # response = delete_license(license_id)
    # if response == "success":
    #     return get_license_data(request)

    # else:
    #     response = HttpResponse(response, content_type="text/plain")
    #     return response
