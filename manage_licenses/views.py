import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.http import HttpResponse, HttpResponseRedirect


from .models import License

#Import contact, entitlement, and organization models from manage_contacts app
from manage_contacts.models import Contact, Entitlement, Organization

from .forms import ProductForm, SearchForm

# Create your views here.

@login_required
def manage_licenses(request):

    current_user = request.user
    user_id = current_user.id
    user_email = current_user.email

    contact_data = Contact.objects.filter(user_id=user_id).get()
    user_role = contact_data.role
    
    org_id = contact_data.organization_id
    org_data = Organization.objects.filter(id=org_id).get()
    user_org = org_data.org_name

    product_entitlements = Entitlement.objects.filter(organization_id=org_id)


    product_licenses = License.objects.filter(org_id=org_id)

    #Change to float and add function for getting number from product
    version_number = 1

    license_list = []

    for product_license in product_licenses:
        product_name = product_license.product_name
        entitlement_data = Entitlement.objects.filter(product_name=product_name).get()
        max_licenses = entitlement_data.max_licenses
        total_licenses = entitlement_data.total_licenses
        num_allocated = str(total_licenses) + " of " + str(max_licenses)

        access_code = "xxxx-xxxx-xxxx"

        license_dict = {}
        license_dict["product_name"] = product_name
        license_dict["access_code"] = access_code
        license_dict["num_allocated"] = num_allocated
        license_list.append(license_dict)

    access_code = "xxxx-xxxx-xxxx"
    entitlement_list =[]
    product_list = []
    for product in product_entitlements:
        product_list.append((product.product_name, product.product_name))

        product_name = product.product_name
        max_licenses = product.max_licenses
        total_licenses = product.total_licenses
        num_allocated = str(total_licenses) + " of " + str(max_licenses)

        entitlement_dict = {}
        entitlement_dict["product_name"] = product_name
        entitlement_dict["access_code"] = access_code
        entitlement_dict["num_allocated"] = num_allocated
        entitlement_list.append(entitlement_dict)

    choice_list = product_list

    search_form = SearchForm()

    if request.GET.get("product_search"):
        print("searching")
        filter_list = []
        user_query = request.GET
        product_search = user_query.get("product_search")
        for product in product_entitlements:
            if product_search.lower() in product.product_name.lower():
                filter_list.append((product.product_name, product.product_name))

        choice_list = filter_list

    if "clear_search" in request.POST:
        choice_list = product_list

    product_form = ProductForm(products=choice_list)
    
    if request.GET.get('product_choice'):
        user_query = request.GET
        product_choice = user_query.get("product_choice")
        entitlement_data = Entitlement.objects.filter(product_name=product_choice).get()
        max_licenses = entitlement_data.max_licenses

        total_licenses = entitlement_data.total_licenses
        used_licenses = max_licenses - total_licenses

        if used_licenses < max_licenses:
            new_license = License(org_id=org_id, 
                                  creation_date=datetime.datetime.now(),
                                  product_name=product_choice,
                                  version=version_number,
                                  creator_address=user_email)
                                  
            new_license.save()

            total_licenses -= 1
            entitlement_data.total_licenses = total_licenses
            entitlement_data.save()
            
            messages.add_message(request, messages.INFO, 'success')
            return HttpResponseRedirect(request.path_info)

        else:
            messages.add_message(request, messages.INFO, 'Not enough licenses')
            return HttpResponseRedirect(request.path_info)

    
    context = {'user_email': user_email,
                'user_role': user_role,
                'organization':user_org,
                'org_id': org_id,
                'entitlements':product_entitlements,
                'licenses': product_licenses,
                'user_products': product_entitlements,
                'product_form':product_form,
                'entitlement_list':entitlement_list,
                'product_entitlements':product_entitlements,
                'search_form':search_form
                }

    return render(request, "manage_licenses/manage-licenses.html", context)
