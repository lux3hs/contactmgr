import datetime

from django.conf import settings
base_dir = settings.BASE_DIR

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from manage_contacts.models import Contact, Entitlement, Organization
from .models import License
from .forms import ChoiceForm, SearchForm, NewLicenseForm

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

    #Create a search form
    search_form = SearchForm()

    #Filter product entitlement list on response from search form
    if request.GET.get("search_query"):
        print("searching")
        # filter_list = []
        entitlement_filter = []
        user_query = request.GET
        product_search = user_query.get("search_query")
        for entitlement in product_entitlements:
            if product_search.lower() in entitlement.product_name.lower():
                print("hello!")
                # filter_list.append((entitlement.product_name, entitlement.product_name))
                
                product_name = entitlement.product_name
                max_licenses = entitlement.max_licenses
                total_licenses = entitlement.total_licenses
                num_allocated = str(total_licenses) + " of " + str(max_licenses)
                entitlement_dict = {}
                entitlement_dict["product_name"] = product_name
                entitlement_dict["access_code"] = access_code
                entitlement_dict["num_allocated"] = num_allocated
                entitlement_filter.append(entitlement_dict)

        # choice_list = filter_list
        entitlement_list = entitlement_filter

    #Clear search filter on response from clear search button (this can be done with just a button!)
    elif request.GET.get("clear_search"):
        return HttpResponseRedirect(request.path_info)

    #Create a product form with product list
    # product_form = ChoiceForm(field_choices=choice_list)

    # product_choices = [("AppLoader", "AppLoader"), ("ScenarioBuilder", "ScenarioBuilder")]
    product_choices = []
    for entitlement in product_entitlements:
        product_choices.append((entitlement.product_name, entitlement.product_name))
        
    new_license_form = NewLicenseForm(product_choices=product_choices)

    #Generate licenses on response from new license form
    # if request.GET.get('field_choice'):
    #     user_query = request.GET
    #     product_choice = user_query.get("field_choice")
    #     entitlement_data = Entitlement.objects.filter(product_name=product_choice).get()
    #     max_licenses = entitlement_data.max_licenses

    #     total_licenses = entitlement_data.total_licenses
    #     used_licenses = max_licenses - total_licenses

       
       
    #     if used_licenses < max_licenses:
    #         new_license = License(org_id=org_id, 
    #                               creation_date=datetime.datetime.now(),
    #                               product_name=product_choice,
    #                               version_number=version_number,
    #                               creator_address=user_email)
                                  
    #         new_license.save()

    #         total_licenses -= 1
    #         entitlement_data.total_licenses = total_licenses
    #         entitlement_data.save()
            
    #         messages.add_message(request, messages.INFO, 'success')
    #         return HttpResponseRedirect(request.path_info)

    #     else:
    #         messages.add_message(request, messages.INFO, 'Not enough licenses')
    #         return HttpResponseRedirect(request.path_info)

    if request.method == "POST":
        user_query = request.POST
        product_choice = user_query.get('product')
        ip_host = user_query.get('iphost')
        creator_email = user_query.get('email')
        creator_phone = user_query.get('phone')

        entitlement_data = product_entitlements.filter(product_name=product_choice).get()

        max_licenses = entitlement_data.max_licenses

        total_licenses = entitlement_data.total_licenses
        used_licenses = max_licenses - total_licenses

        is_permanent = True
        product_grade = "standard"
        product_stations = 10000
        allowed_ips = 10        
        
        weeks_allocated = 2
        expire_time = datetime.timedelta(weeks = weeks_allocated)

        if used_licenses < max_licenses:
            new_license = License(org_name=user_org,
                                  org_id=org_id, 
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

            total_licenses -= 1
            entitlement_data.total_licenses = total_licenses
            entitlement_data.save()


    # if request.GET.get("license_selection"):
    #     user_selection = request.GET
    #     print(user_selection.get("license_selection"))

    if request.GET.get('delete_license'):
        user_selection = request.GET
        license_id = user_selection.get("license_selection")
        license_selection = product_licenses.filter(id=license_id)
        license_selection.delete()

        # license_id = user_selection.get("license_selection")
        # print(product_licenses.filter(id=license_id))

    if request.GET.get("download_license"):
        user_selection = request.GET
        license_id = user_selection.get("license_selection")

        license_dict = {}

        try:
            license_selection = product_licenses.filter(id=license_id).get()

            license_dict["userID"] = user_id
            license_dict["Email"] = user_email
            license_dict["Organization"] = license_selection.org_name
            license_dict["Host/IP"] = license_selection.IP_Host
            license_dict["Version"] = license_selection.version_number
            license_dict["Creation Date"] = license_selection.creation_date
            license_dict["Expiration Date"] = license_selection.expiration_date
            license_dict["Success"] = True

        except:
            license_dict["Success"] = False

        
        license_data = ""
        for field in license_dict:
            print(field)
            license_data = license_data + str(field) + ": " + str(license_dict[field]) + "\n"

        #Add a key of encrypted license data
        license_key = "userKey"
        license_data = license_data + "Key=" + license_key


        response = HttpResponse(license_data, content_type="text/plain")
        response['Content-Disposition'] = 'attachment; filename="product-license.lic"'
        return response
        
    
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
    license_file = str(base_dir) + "/bin/licenseserver.lic"
    f = open(license_file, "r")
    license_data = f.read()
    license_name = "product-license"

    license_path = str(base_dir) + "/bin/" + license_name + ".lic"
    license_data = open(license_path, "w")
    license_data.write("licenseInfo")
    license_data.close()

    license_data = license_data.replace("\n", "\r\n")
    user_selection = request.POST
    print(user_selection)

    license_data = "License Data"
    response = HttpResponse(license_data, content_type="text/plain")
    response['Content-Disposition'] = 'attachment; filename="product-license.lic"'
    return response