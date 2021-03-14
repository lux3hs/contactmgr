import datetime
import os.path

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from manage_contacts.models import Contact, Product, Entitlement, Organization
from .models import License
from .forms import ChoiceForm, SearchForm, NewLicenseForm
from django.conf import settings

base_dir = str(settings.BASE_DIR)


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
        product_name = entitlement.product.product_name
        max_licenses = entitlement.max_licenses
        total_licenses = entitlement.total_licenses
        num_allocated = str(total_licenses) + " of " + str(max_licenses)
        entitlement_dict = {}
        entitlement_dict["product_name"] = product_name
        entitlement_dict["access_code"] = access_code
        entitlement_dict["num_allocated"] = num_allocated
        entitlement_list.append(entitlement_dict)

    #Create a search form
    search_form = SearchForm()

    #Filter product entitlement list on response from search form
    if request.GET.get("search_query"):
        entitlement_filter = []
        user_query = request.GET
        product_search = user_query.get("search_query")
        for entitlement in product_entitlements:
            entilement_product = entitlement.product

            if product_search.lower() in entilement_product.product_name.lower():
                product_name = entitlement.product_name
                max_licenses = entitlement.max_licenses
                total_licenses = entitlement.total_licenses
                num_allocated = str(total_licenses) + " of " + str(max_licenses)
                entitlement_dict = {}
                entitlement_dict["product_name"] = product_name
                entitlement_dict["access_code"] = access_code
                entitlement_dict["num_allocated"] = num_allocated
                entitlement_filter.append(entitlement_dict)

        entitlement_list = entitlement_filter

    #Clear search filter on response from clear search button (This can be done with just a button!)
    elif request.GET.get("clear_search"):
        return HttpResponseRedirect(request.path_info)

    #Create product choices from user entitlements
    product_choices = []
    for entitlement in product_entitlements:
        product_choices.append((entitlement.product.product_name, entitlement.product.product_name))

    #Create a form for license generation
    new_license_form = NewLicenseForm(product_choices=product_choices)

    #Generate license on response from form
    if request.method == "POST":
        user_query = request.POST
        product_choice = user_query.get('product_choice')
        ip_host = user_query.get('ip_host')
        creator_email = user_query.get('creator_email')
        creator_phone = user_query.get('creator_phone')

        #Get entitlement data
        entitlement_product = Product.objects.filter(product_name=product_name).get()
        product_id = entitlement_product.id
        entitlement_data = product_entitlements.filter(product=product_id).get()

        #Get max/total licenses and calculate difference
        max_licenses = entitlement_data.max_licenses
        total_licenses = entitlement_data.total_licenses
        used_licenses = max_licenses - total_licenses

        #Create license if entitlements exist
        if used_licenses < max_licenses:
            #These variables should be passed in instead of hardcoded
            is_permanent = True
            product_grade = "standard"
            product_stations = 10000
            allowed_ips = 10        
            weeks_allocated = 2
            expire_time = datetime.timedelta(weeks = weeks_allocated)
            new_license = License(org_name=user_org,
                                  org_id=org_id,
                                  entitlement_id=entitlement_data.id,
                                  IP_Host=ip_host,
                                  creator_email=creator_email,
                                  creator_phone=creator_phone,
                                  product_name=product_choice,
                                  version_number=version_number,
                                  is_permanent=is_permanent,
                                  product_grade=product_grade,
                                  product_stations=product_stations,
                                  allowed_ips=allowed_ips,
                                  creation_date=datetime.datetime.now(),
                                  expiration_date=datetime.datetime.now() + expire_time,
            )
                                  
            new_license.save()

            #Reduce license allocations after successful generation
            total_licenses -= 1
            entitlement_data.total_licenses = total_licenses
            entitlement_data.save()

            messages.add_message(request, messages.INFO, 'New license created')
            return HttpResponseRedirect(request.path_info)

        else:
            messages.add_message(request, messages.INFO, 'Not enough product entitlements')
            return HttpResponseRedirect(request.path_info)

    #Check for input for delete license
    if request.GET.get('delete_license_selection'):
        user_selection = request.GET.getlist("license_selection")
        for license_id in user_selection:
            license_selection = product_licenses.filter(id=license_id)
            
            license_object = license_selection.get()
            entitlement_id = license_object.entitlement_id
            entitlement_data = product_entitlements.filter(id=entitlement_id).get()
            entitlement_data.total_licenses += 1
            entitlement_data.save()

            license_selection.delete()

            messages.add_message(request, messages.INFO, 'Selection Deleted')
            return HttpResponseRedirect(request.path_info)

    # if request.GET.get('delete_single_license'):
    #     user_selection = request.GET.get('delete_single_license')
    #     license_id = user_selection
    #     license_selection = product_licenses.filter(id=license_id)
    #     license_object = license_selection.get()
    #     entitlement_id = license_object.entitlement_id
    #     entitlement_data = product_entitlements.filter(id=entitlement_id).get()
    #     entitlement_data.total_licenses += 1
    #     entitlement_data.save()
    #     license_selection.delete()
    #     messages.add_message(request, messages.INFO, 'License Deleted')
    #     return HttpResponseRedirect(request.path_info)

    #Check for input for generate license
    if request.GET.get("generate_license_selection"):
        user_selection = request.GET.getlist("license_selection")
        license_data = ""
        for license_id in user_selection:
            try:
                license_dict = {}
                license_selection = product_licenses.filter(id=license_id).get()
                license_dict["Product"] = license_selection.product_name
                license_dict["Organization"] = license_selection.org_name
                license_dict["Host/IP"] = license_selection.IP_Host
                license_dict["Version"] = license_selection.version_number
                license_dict["userID"] = user_id
                license_dict["Email"] = user_email
                license_dict["Creation Date"] = license_selection.creation_date
                license_dict["Expiration Date"] = license_selection.expiration_date
                
                license_selection.delete()
                
                temp_data = ""
                for field in license_dict:
                    temp_data = temp_data + str(field) + ": " + str(license_dict[field]) + "\n"
                    
                temp_data = temp_data + "\n"
                license_data = license_data + temp_data

                license_dict["Success"] = True

            except:
                license_dict["Success"] = False
                break

        if license_dict["Success"] == True:
        
            #Add a key of encrypted license data (Need to add function for encryption here)
            license_key = "userKey"
            license_data = license_data + "Key=" + license_key

            license_file = base_dir + "/bin/Product-License.lic"
            f = open(license_file, "w")
            f.write(license_data)
            f.close()
            
            messages.add_message(request, messages.INFO, 'Selection Generated Successfully')
            return HttpResponseRedirect(request.path_info)

        else:
            messages.add_message(request, messages.INFO, 'Selection generation failed')
            return HttpResponseRedirect(request.path_info)
        

    # if request.GET.get('generate_single_license'):
    #     user_selection = request.GET.get('generate_single_license')
    #     license_id = user_selection
    #     license_data = ""
    #     license_dict = {}

    #     try:
    #         license_dict = {}
    #         license_selection = product_licenses.filter(id=license_id).get()
    #         license_dict["Product"] = license_selection.product_name
    #         license_dict["Organization"] = license_selection.org_name
    #         license_dict["Host/IP"] = license_selection.IP_Host
    #         license_dict["Version"] = license_selection.version_number
    #         license_dict["userID"] = user_id
    #         license_dict["Email"] = user_email
    #         license_dict["Creation Date"] = license_selection.creation_date
    #         license_dict["Expiration Date"] = license_selection.expiration_date

    #         license_selection.delete()

    #         license_dict["Success"] = True

    #     except:
    #         license_dict["Success"] = False


    #     temp_data = ""
    #     for field in license_dict:
    #         temp_data = temp_data + str(field) + ": " + str(license_dict[field]) + "\n"

    #     temp_data = temp_data + "\n"
    #     license_data = license_data + temp_data

    #     #Add a key of encrypted license data (Need to add function for encryption here)
    #     license_key = "userKey"
    #     license_data = license_data + "Key=" + license_key


    #     license_file = str(base_dir) + "/bin/Product-License.lic"
    #     f = open(license_file, "w")
    #     f.write(license_data)
    #     f.close()
        
    #     messages.add_message(request, messages.INFO, 'License Generated Successfully')
    #     return HttpResponseRedirect(request.path_info)
    
    #Render variables in html
    context = {'user_email': user_email,
                'user_role': user_role,
                'user_org':user_org,
                'org_id': org_id,
                'product_licenses': product_licenses,
                'user_products': product_entitlements,
                # 'product_form':product_form,
                'entitlement_list':entitlement_list,
                'search_form':search_form,
                'new_license_form':new_license_form,
                }

    return render(request, "manage_licenses/manage-licenses.html", context)


def download_license(request):
    # BASE_DIR = os.path.dirname(os.path.dirname(__file__))
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
