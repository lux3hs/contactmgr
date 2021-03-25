import datetime
import os.path

import json

from django.contrib.auth.models import User


from .models import License
from manage_contacts.models import Contact, Product, Entitlement, Organization

from django.conf import settings

base_dir = str(settings.BASE_DIR)



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
        
        return True

    except:
        return False

def delete_license(license_id):
    """ Delete license object from database """
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


def package_license_data(license_values):
    product_licenses = License.objects.all()
    data_string = ""
    for license_id in license_values:
        license_selection = product_licenses.filter(id=license_id).get()
        license_data = license_selection.get_package_data()
        data_string += str(license_data) + "\n"

    return data_string

def check_license_data(license_selection):
    for license_id in license_selection:
        license_check = License.objects.filter(id=license_id)
        if len(license_check) > 0:
            pass

        else:
            return False

    return True



def generate_license_key(license_data):
    license_key = license_data + 'MyKey="EncryptedData"'
    return license_key


def get_table_data(table_header, object_data):
    """ Create a data object to pass into tables """
    data = {}
    header_list = []
    for key in table_header.keys():
        header_list.append(table_header[key])
    
    data['table_header'] = header_list
    if len(object_data) > 0:
        data_list = []
        for obj in object_data:
            try:
                object_dictionary = obj.get_table_dictionary()
                temp_dict = {}
                temp_dict["data_id"] = object_dictionary.get("data_id")
                for key in table_header.keys():
                    if key in object_dictionary.keys():
                        temp_dict[key] = object_dictionary.get(key)
                    
                    else:
                        temp_dict[key] = "error"

                data_list.append(temp_dict)

                data['table_data'] = data_list
                data['Success'] = True

            except:
                data['Success'] = False

    return data
                    


def get_license_header():
    license_header = {'id':'ID',
                    'product_name':'Product',
                    'version_number':'Version',
                    'org_name':'Org', 
                    'IP_Host':'IP Host', 
                    'creator_email': 'Email', 
                    'is_permanent': 'Permanent',
                    'product_grade': 'Grade',
                    'product_stations': 'Stations',
                    'creation_date': 'Created',
                    'expiration_date': 'Expires',
                    }

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
