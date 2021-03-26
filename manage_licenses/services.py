import datetime
import os
import os.path

from django.conf import settings
from django.utils.dateparse import parse_datetime

from .models import License
from manage_contacts.models import Contact, Product, Entitlement

#Set base directory
base_dir = str(settings.BASE_DIR)

##Basic service methods

def get_choice_list(model_header):
    """ Build list of choices based on model header """
    choice_list = []
    for key in model_header:
        choice_list.append((key, model_header[key]))

    return choice_list


##Keygen services

def exec_arg(arg):
    """ execute a string as an argument """
    os.system(arg)

def generate_license_key(data_package):
    """ Run AlKeyMaker.exe on license string """
    run_dir = base_dir + "/bin/"
    file_dir = base_dir + "/bin/keygen/"
    data_string = data_package['data_string']
    key_name = str(data_package['key_name']) + ".txt"
    
    exec_string = ("wine " + run_dir +
                   "AlKeyMaker.exe string=" +
                   '"' + str(data_string) + '"' +
                   " flag=encrypt outputfile=" +
                   file_dir + key_name)

    try:
        exec_arg(exec_string)
        return key_name

    except: 
        return None


def read_key_file(key_name):
    """ Read file created by AlKeyMaker.exe """
    file_dir = base_dir + "/bin/keygen/" + key_name
    f = open(file_dir, "r")
    key_text = f.read()
    return key_text


def package_license_data(license_id):
    """ Package license data for download """
    license_selection = License.objects.filter(id=license_id).get()
    data_string = ""
    key_name = ""
    # for license_id in license_values:
    key_name = license_id
    # license_selection = product_licenses.filter(id=license_id).get()
    license_data = license_selection.get_package_data()
    data_string += str(license_data) + "\n"

    data_package = {'key_name':key_name, 'data_string':data_string}

    return data_package


def check_license_data(license_selection):
    """ Check license data for integrity """
    if len(license_selection) > 0:
        for license_id in license_selection:
            license_check = License.objects.filter(id=license_id)
            if len(license_check) > 0:
                pass

            else:
                return False

        return True

    else: 
        return False


##Model object services##

def create_license(current_user, user_query):
    """ Create new license on user request """
    user_id = current_user.id


    contact_data = Contact.objects.filter(user=user_id).get()

    creator_email = contact_data.user.email
    creator_phone = contact_data.phone
    user_org = contact_data.organization.org_name
    org_id = contact_data.organization.id
    
    product_name = user_query.get('product_name')
    host_ip = user_query.get('host_ip')
    product_grade = user_query.get("product_grade")
    product_stations = user_query.get("product_stations")

    expiration_date = user_query.get('expiration_date')
    clean_date = parse_datetime(expiration_date)
    expiration_date = clean_date

    allowed_ips = user_query.get('allowed_ips')
    re_seller = user_query.get('re_seller')

    entitlement_product = Product.objects.filter(product_name=product_name).get()
    product_id = entitlement_product.id
    product_version = entitlement_product.product_version
    entitlement_data = Entitlement.objects.filter(organization=org_id, product=product_id).get()
    entitlement_id = entitlement_data.id

    is_permanent = user_query.get('is_permanent')
    if is_permanent:
        is_permanent = True
    
    else:
        is_permanent = False
    
    new_license = License(org_name=user_org,
                            org_id=org_id,
                            entitlement_id=entitlement_id,
                            creator_email=creator_email,
                            creator_phone=creator_phone,
                            re_seller=re_seller,
                            product_name=product_name,
                            version_number=product_version,
                            host_ip=host_ip,
                            is_permanent=is_permanent,
                            product_grade=product_grade,
                            product_stations=product_stations,
                            allowed_ips=allowed_ips,
                            creation_date=datetime.datetime.now(),
                            expiration_date=expiration_date,
    )

    new_license.save()
    
    return new_license


def delete_license_data(license_selection):
    """ Delete license selection from database """
    print(license_selection)

    for license_id in license_selection:
        try:
            license_data = License.objects.filter(id=license_id).get()
            entitlement_id = license_data.entitlement_id
            entitlement_data = Entitlement.objects.filter(id=entitlement_id).get()

            license_data.delete()
            entitlement_data.add_license()
        
        except:
            return license_id

    return True




## JS Table Services ##

def get_license_header():
    """ Get license table header """
    license_header = {'id':'ID',
                    'product_name':'Product',
                    'version_number':'Version',
                    'org_name':'Org', 
                    'host_ip':'Host IP', 
                    'creator_email': 'Email', 
                    'is_permanent': 'Permanent',
                    'product_grade': 'Grade',
                    'product_stations': 'Stations',
                    'creation_date': 'Created',
                    'expiration_date': 'Expires',
                    }

    return license_header


def get_entitlement_header():
    """ Get entitlement table header """
    entitlement_header = {'product_name':'Product',
                          'product_version':'Version',
                          'num_allocated':'Allocated', 
                          }

    return entitlement_header


#Create table data based on header keys and object data#
## Data model must have get_table_dictionary function ##
def get_table_data(table_header, object_data):
    """ Create a data object to populate table """
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
