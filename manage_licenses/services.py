import datetime
import os.path


from .models import License
from manage_contacts.models import Contact, Product, Entitlement, Organization

from django.conf import settings

base_dir = str(settings.BASE_DIR)


# def check_entitlements(org, product):

#     print("hello")
#     entitlement_data = Entitlement.objects.filter(organization=org, product=product).get()
#     if check_entitlements(org, product)


#     print(entitlement_data.max_licenses)
#     print(entitlement_data.total_licenses)


def create_license(current_user, user_query):
    try:
        # current_user = request.user
        user_id = current_user.id
        creator_email = current_user.email
        contact_data = Contact.objects.filter(user=user_id).get()
        org_object = contact_data.organization
        user_org = org_object.org_name
        org_id = org_object.id
        org_id = contact_data.organization.id

        
        
        
        
        product_choice = user_query.get('product_choice')
        ip_host = user_query.get('ip_host')
        # check_entitlements(current_user.org, product_choice)
        
        #Get entitlement data for current contact organization
        entitlement_product = Product.objects.filter(product_name=product_choice).get()
        product_id = entitlement_product.id

        product_version = entitlement_product.product_version
        entitlement_data = Entitlement.objects.filter(organization=org_id, product=product_id).get()
        entitlement_id = entitlement_data.id

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

        new_license.save()

        entitlement_data.total_licenses -= 1
        entitlement_data.save()
        
        return "New license created"

    except:
        return "error"

def delete_license(license_id):
    """ Delete license object from database based on user selection """
    # current_user = request.user
    if (license_id):
        try:
            license_selection = License.objects.filter(id=license_id)
            license_selection.delete()

            return True

        except:
            return False

    else:
        return False

def generate_license_array(current_user, user_selection):
    """ Generate license files for download """
    print(user_selection)
    user_id = current_user.id
    contact_data = Contact.objects.filter(user=user_id).get()
    org_object = contact_data.organization

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
                license_dict = license_selection.get_table_dictionary()

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
            license_array["Message"] = "error"


    return license_array

def generate_license_key(license_data):
    print("I need a function to encrypt " + license_data)
    return "MyLicenseKey"



def get_table_data(table_header, object_data):
    """ Create a data object to pass into tables """
    data = {}
    header_list = []
    for key in table_header.keys():
        header_list.append(table_header[key])
    
    data['table_header'] = header_list
    if len(object_data) > 0:
        try:
            data_list = []
            for obj in object_data:
                object_dictionary = obj.get_table_dictionary()
                temp_dict = {}
                temp_dict["data_id"] = object_dictionary.get("data_id")
                for key in table_header.keys():
                    if key in object_dictionary.keys():
                        temp_dict[key] = object_dictionary.get(key)

                data_list.append(temp_dict)

            data['table_data'] = data_list
            data['Success'] = True

        except:
            data['Success'] = False

    return data
                    


def get_license_header():
    license_header = {'product_name':'Product',
                    'version_number':'Version',
                    'org_name':'Org', 
                    'IP_Host':'IP Host', 
                    'creator_email': 'Email', 
                    'is_permanent': 'Permanent',
                    'product_grade': 'Grade',
                    'product_stations': 'Stations',
                    'creation_date': 'Created',
                    'expiration_date': 'Expires'}

    return license_header


def get_entitlement_header():
    entitlement_header = {'product_name':'Product',
                          'product_version':'Version',
                          'num_allocated':'Allocated', 
                          }

    return entitlement_header



def get_choice_list(model_header):
    choice_list = []
    for key in model_header:
        choice_list.append((key, model_header[key]))

    return choice_list

