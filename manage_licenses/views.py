import datetime

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from manage_contacts.models import Contact, Entitlement, Organization
from .models import License
from .forms import ChoiceForm, SearchForm

# Create your views here.

@login_required
def manage_licenses(request):
    """ Render manage-licenses html page """
    #This should be passed in somewhere instead of hardcoded (Created by user on license generation?)
    version_number = "v0.10"
    access_code = "xxxx-xxxx-xxxx"
    
    #Get current user info
    current_user = request.user
    user_id = current_user.id
    user_email = current_user.email
    contact_data = Contact.objects.filter(user_id=user_id).get()
    user_role = contact_data.role
    org_id = contact_data.organization_id
    org_data = Organization.objects.filter(id=org_id).get()
    user_org = org_data.org_name

    #Get entitlement data for current contact
    product_entitlements = Entitlement.objects.filter(organization_id=org_id)
    product_licenses = License.objects.filter(org_id=org_id)

    #Create list of entitlement data to display in table
    entitlement_list = []
    for entitlement in product_entitlements:
        product_name = entitlement.product_name
        max_licenses = entitlement.max_licenses
        total_licenses = entitlement.total_licenses
        num_allocated = str(total_licenses) + " of " + str(max_licenses)
        entitlement_dict = {}
        entitlement_dict["product_name"] = product_name
        entitlement_dict["access_code"] = access_code
        entitlement_dict["num_allocated"] = num_allocated
        entitlement_list.append(entitlement_dict)

    #Create list of products
    product_list = []
    for product in product_entitlements:
        product_list.append((product.product_name, product.product_name))
    
    choice_list = product_list

    #Create a search form
    search_form = SearchForm()

    #Filter product list on response from search form
    if request.GET.get("search_query"):
        print("searching")
        filter_list = []
        user_query = request.GET
        product_search = user_query.get("search_query")
        for entitlement in product_entitlements:
            if product_search.lower() in entitlement.product_name.lower():
                print("hello!")
                filter_list.append((entitlement.product_name, entitlement.product_name))

        choice_list = filter_list

    #Clear search filter on response from clear search button
    elif request.GET.get("clear_search"):
        return HttpResponseRedirect(request.path_info)

    #Create a product form with product list
    product_form = ChoiceForm(field_choices=choice_list)

    #Generate licenses on response from product form
    if request.GET.get('field_choice'):
        user_query = request.GET
        product_choice = user_query.get("field_choice")
        entitlement_data = Entitlement.objects.filter(product_name=product_choice).get()
        max_licenses = entitlement_data.max_licenses

        total_licenses = entitlement_data.total_licenses
        used_licenses = max_licenses - total_licenses

        if used_licenses < max_licenses:
            new_license = License(org_id=org_id, 
                                  creation_date=datetime.datetime.now(),
                                  product_name=product_choice,
                                  version_number=version_number,
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

    
    #Render variables in html
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
