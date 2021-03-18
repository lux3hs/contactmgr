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
from .forms import ChoiceForm, SearchForm, NewLicenseForm
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
    org_id = user_org.id
    org_name = user_org.org_name

    # org_object = contact_data.get_contact_org()
    # user_org = org_object.org_name
    # org_id = org_object.id

    #Get entitlement data for current contact organization
    product_entitlements = Entitlement.objects.filter(organization=org_id)

    #Get product data for current contact organization
    product_licenses = License.objects.filter(org_id=org_id)

    #Create list of entitlement data to display in table
    # entitlement_list = []
    # for entitlement in product_entitlements:
    #     entitlement_dict = entitlement.get_entitlement_dictionary()
    #     entitlement_list.append(entitlement_dict)

    # new_dictionary = {'entitlements': entitlement_list}
    # new_string = dumps(new_dictionary)

    #Create a search form
    search_form = SearchForm()

    #Filter product entitlement list on response from search form
    # if request.GET.get("search_query"):
    #     entitlement_filter = []
    #     user_query = request.GET
    #     product_search = user_query.get("search_query")
    #     for entitlement in product_entitlements:
    #         entilement_product = entitlement.product

    #         if product_search.lower() in entilement_product.product_name.lower():
    #             entitlement_dict = entitlement.get_entitlement_dictionary()
    #             entitlement_filter.append(entitlement_dict)

    #     entitlement_list = entitlement_filter

    #     new_dictionary = {'entitlements': entitlement_list}
    #     new_string = dumps(new_dictionary)
    #     print(new_string)

    
    #Clear search filter on response from clear search button
    if request.GET.get("clear_search"):
        return HttpResponseRedirect(request.path_info)

    #Create product choices from entitlements
    product_choices = []
    for entitlement in product_entitlements:
        product_choices.append((entitlement.product.product_name, entitlement.product.product_name))

    #Create a form for license generation
    new_license_form = NewLicenseForm(product_choices=product_choices)

    #Generate license on response from form
    if request.method == "POST":
        user_query = request.POST
        product_choice = user_query.get('product_choice')

        #Get entitlement data
        entitlement_product = Product.objects.filter(product_name=product_choice).get()
        product_id = entitlement_product.id
        entitlement_data = product_entitlements.filter(product=product_id).get()

        #Create license if entitlements exist
        if entitlement_data.check_allocated_licenses():
            new_license = create_license(current_user, user_query)
            new_license.save()
                                
            #Reduce license allocations after successful generation
            entitlement_data.total_licenses -= 1
            entitlement_data.save()

            messages.add_message(request, messages.INFO, 'New license created')
            return HttpResponseRedirect(request.path_info)

        else:
            messages.add_message(request, messages.INFO, 'Not enough product entitlements')
            return HttpResponseRedirect(request.path_info)

    #Check for input from delete license
    if request.GET.get('delete_license_selection'):
        user_selection = request.GET.getlist("license_selection")
        delete_license(current_user, user_selection)   
        messages.add_message(request, messages.INFO, 'Selection Deleted')
        return HttpResponseRedirect(request.path_info)

    #Check for input from generate license
    if request.GET.get("generate_license_selection"):
        user_selection = request.GET.getlist("license_selection")
        license_array = generate_license_array(current_user, user_selection)
        messages.add_message(request, messages.INFO, license_array["Message"])
        return HttpResponseRedirect(request.path_info)
    
    #Render variables in html
    context = {'user_email': user_email,
                'user_role': user_role,
                'user_org':org_name,
                'org_id': org_id,
                'product_licenses': product_licenses,
                'user_products': product_entitlements,
                # 'product_form':product_form,
                # 'entitlement_list':entitlement_list,
                'search_form':search_form,
                'new_license_form':new_license_form,
                }

    return render(request, "manage_licenses/manage-licenses.html", context)


def download_license(request):
    """ Download a generated license """
    license_file = base_dir + "/bin/Product-License.lic"
    if os.path.isfile(license_file):
        f = open(license_file, "r")
        license_data = f.read()
        os.remove(license_file)
        license_data = license_data.replace("\n", "\r\n")
        response = HttpResponse(license_data, content_type="text/plain")
        response['Content-Disposition'] = 'attachment; filename="product-license.lic"'
        return response

    else:
        response = HttpResponse("No file exists", content_type="text/plain")
        return response


def get_entitlement_data(request):
    #Get current user info
    current_user = request.user
    user_id = current_user.id
    # user_email = current_user.email
    contact_data = Contact.objects.filter(user=user_id).get()
    # user_role = contact_data.role
    org_object = contact_data.get_contact_org()
    # user_org = org_object.org_name
    org_id = org_object.id

    #Get entitlement data for current contact organization
    product_entitlements = Entitlement.objects.filter(organization=org_id)
    entitlement_list = []
    try:
        for entitlement in product_entitlements:
            table_dict = entitlement.get_table_dictionary()
            entitlement_list.append(table_dict)

        table_headers = product_entitlements[0].get_table_headers()
        success = True
    
    except:
        success = False

    data = {'table_data': entitlement_list, 'table_headers':table_headers, 'success':success}

    return JsonResponse(data)



def get_license_data(request):
    print("hello")
    # current_user = request.user
    # user_id = current_user.id
    # contact_data = Contact.objects.filter(user=user_id).get()
    # user_org = contact_data.organization
    # org_id = user_org.id
    
    # # org_object = contact_data.get_contact_org()
    # # org_id = org_object.id
    # product_licenses = License.objects.filter(org_id=org_id)
    # license_list = []
    # try:
    #     for product_license in product_licenses:
    #         table_dict = product_license.get_license_dictionary()
    #         license_list.append(table_dict)

    #     table_headers = product_licenses[0].get_table_headers()
    #     success = True
    
    # except:
    #     success = False

    # data = {'table_data': product_licenses, 'table_headers':table_headers, 'success':success}

    # return JsonResponse(data)


    # product_licenses = License.objects.filter(org_id=org_id)

    response = HttpResponse("No file exists", content_type="text/plain")
    return response