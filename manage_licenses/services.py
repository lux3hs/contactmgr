import datetime
import os.path

from .models import License
from manage_contacts.models import Contact, Product, Entitlement, Organization

from django.conf import settings

base_dir = str(settings.BASE_DIR)


def create_license(current_user, user_query):
    # current_user = request.user
    user_id = current_user.id
    creator_email = current_user.email
    contact_data = Contact.objects.filter(user=user_id).get()
    org_object = contact_data.get_contact_org()
    user_org = org_object.org_name
    org_id = org_object.id

    product_choice = user_query.get('product_choice')
    ip_host = user_query.get('ip_host')

    #Get entitlement data for current contact organization
    entitlement_product = Product.objects.filter(product_name=product_choice).get()
    product_id = entitlement_product.id
    product_version = entitlement_product.product_version
    product_entitlement = Entitlement.objects.filter(organization=org_id, product=product_id).get()
    entitlement_id = product_entitlement.id

    is_permanent = user_query.get("is_permanent")
    if is_permanent:
        is_permanent = True
    
    else:
        is_permanent = False

    #These values should be passed in
    weeks_allocated = 2
    expire_time = datetime.timedelta(weeks = weeks_allocated)

    product_grade = "standard"
    product_stations = 10000
    allowed_ips = 10
    
    new_license = License(org_name=user_org,
                            org_id=org_id,
                            entitlement_id=entitlement_id,
                            IP_Host=ip_host,
                            creator_email=creator_email,
                            product_name=product_choice,
                            version_number=product_version,
                            is_permanent=is_permanent,
                            product_grade=product_grade,
                            product_stations=product_stations,
                            allowed_ips=allowed_ips,
                            creation_date=datetime.datetime.now(),
                            expiration_date=datetime.datetime.now() + expire_time,
    )
                            
    return new_license

def delete_license(current_user, user_selection):
    # current_user = request.user
    user_id = current_user.id
    contact_data = Contact.objects.filter(user=user_id).get()
    org_object = contact_data.get_contact_org()
    org_id = org_object.id

    #Get entitlement data for current contact organization
    product_entitlements = Entitlement.objects.filter(organization=org_id)

    #Get product data for current contact organization
    product_licenses = License.objects.filter(org_id=org_id)
    for license_id in user_selection:
        license_selection = product_licenses.filter(id=license_id)
        
        license_object = license_selection.get()
        entitlement_id = license_object.entitlement_id
        entitlement_data = product_entitlements.filter(id=entitlement_id).get()
        entitlement_data.total_licenses += 1
        entitlement_data.save()

        license_selection.delete()

    return True

def generate_license_array(current_user, user_selection):
    user_id = current_user.id
    contact_data = Contact.objects.filter(user=user_id).get()
    org_object = contact_data.get_contact_org()
    org_id = org_object.id
    product_licenses = License.objects.filter(org_id=org_id)

    license_data = ""
    license_array = {}
    license_file = base_dir + "/bin/Product-License.lic"
    if os.path.isfile(license_file):
        license_array["Success"] = False
        license_array["Message"] = "File exists"

    else:
        try:
            for license_id in user_selection:
                license_selection = product_licenses.filter(id=license_id).get()
                license_dict = license_selection.get_license_dictionary()

                temp_data = ""
                for field in license_dict:
                    temp_data = temp_data + str(field) + ": " + str(license_dict[field]) + "\n"
                    
                temp_data = temp_data + "\n"
                license_data = license_data + temp_data

                license_selection.delete()

            license_key = generate_license_key(license_data)            
            license_data = license_data + "Key=" + license_key

            license_file = base_dir + "/bin/Product-License.lic"
            f = open(license_file, "w")
            f.write(license_data)
            f.close()
                
            license_array["Data"] = license_data
            license_array["Success"] = True
            license_array["Message"] = "File successfully generated"

        except:
            license_array["Success"] = False
            license_array["Message"] = "File generation failed"


    return license_array


def generate_license_key(license_data):
    print("I need a function to encrypt " + license_data)
    return "MyLicenseKey"


