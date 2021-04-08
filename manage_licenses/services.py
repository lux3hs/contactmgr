import os
import os.path

import datetime

from django.conf import settings

from .models import License

#Set base directory
BASE_DIR = str(settings.BASE_DIR)

def package_license_data(license_data):
    """ Package license data for download """
    header_string = ""
    key_name = ""
    key_name = license_data.id
    license_header = license_data.get_license_header()
    for key in license_header.keys():
        header_string += str(key) + str(license_header[key]) + "\r\n"

    data_string = license_data.get_key_string()
    data_package = {'key_name':key_name, 'header_string':header_string, 'data_string':data_string}
    return data_package


def package_master_data(user_query, contact_data, entitlement_choice):
    ml_ID = str(entitlement_choice.id)
    ml_org_name = str(entitlement_choice.organization.org_name)
    ml_org_host_IP = str(user_query.get('host_ip'))
    ml_email = str(contact_data.user.email)
    ml_phone = str(contact_data.phone)

    master_header = ('Master License ID: ' + ml_ID + "\r\n" +
                'Organization Name: ' + ml_org_name + "\r\n" +
                'Organization Host/IP: ' + ml_org_host_IP + "\r\n" +
                'Email Address: ' + ml_email + "\r\n" +
                'Phone Number: ' + ml_phone + "\r\n")

    product_name = entitlement_choice.product.product_name
    product_version = entitlement_choice.product.product_version

    product_stations = str(user_query.get('product_stations'))
    product_grade = str(user_query.get('product_grade'))
    support_id = str(entitlement_choice.id)
    expiration_date = str(user_query.get('expiration_date'))

    entitlement_string = ("Product Name: " + product_name + ", " +
                        "Host/Ip address: " + ml_org_host_IP + ", " +
                        "Version: " + product_version + ", " +
                        "Num of stations: " + product_stations + ", " +
                        "Permanent License, " +
                        "Grade: " + product_grade + ", " +
                        "User name: all, " +
                        "Support ID: " + support_id + ", " +
                        "Support Expiration Date: " + expiration_date + "\r\n")

    master_key_string = 'masterip=' + str(ml_org_host_IP) + "&masterid=" + str(ml_ID)

    key_name = "ml_" + str(entitlement_choice.id)

    master_data = {'key_name':key_name, 
                'entitlement_string':entitlement_string, 
                'master_header': master_header, 
                'data_string':master_key_string}

    return master_data


def generate_license_key(data_package):
    """ Run AlKeyMaker.exe on license string """
    run_dir = BASE_DIR + "/bin/"
    file_dir = BASE_DIR + "/bin/keygen/"
    data_string = data_package['data_string']
    key_name = str(data_package['key_name']) + ".txt"
    
    exec_string = ("wine " + run_dir +
                   "AlKeyMaker.exe string=" +
                   '"' + str(data_string) + '"' +
                   " flag=encrypt outputfile=" +
                   file_dir + key_name)
                   
    try:
        os.system(exec_string)
        return key_name

    except: 
        return None


def read_key_file(key_name):
    """ Read file created by AlKeyMaker.exe """
    file_dir = BASE_DIR + "/bin/keygen/" + key_name
    f = open(file_dir, "r")
    key_text = f.read()
    if "Key=" in key_text:
        coded_key = key_text[key_text.index("Key=") + 4 : len(key_text)]

    else:
        coded_key = False

    return coded_key


def add_new_license(contact_data, entitlement_data, user_query):
    creator_email = contact_data.user.email
    creator_phone = contact_data.phone

    product_name = entitlement_data.product.product_name
    product_version = entitlement_data.product.product_version
    org_name = entitlement_data.organization.org_name

    host_ip = user_query.get('host_ip')
    product_grade = user_query.get("product_grade")
    product_stations = user_query.get("product_stations")
    allowed_ips = user_query.get('allowed_ips')
    re_seller = user_query.get('re_seller')

    is_permanent = user_query.get('is_permanent')
    if is_permanent:
        is_permanent = True
    
    else:
        is_permanent = False

    creation_date = datetime.datetime.now().replace(microsecond=0)
    
    exp_date_string = user_query.get('expiration_date')
    exp_date_strp = datetime.datetime.strptime(exp_date_string, "%m/%d/%Y")
    expiration_date = datetime.datetime.combine(exp_date_strp.date(), creation_date.time())

    new_license = License(org_name=org_name,
                          product_name=product_name,
                          product_version=product_version,
                          creator_email=creator_email,
                          creator_phone=creator_phone,
                          re_seller=re_seller,
                          host_ip=host_ip,
                          is_permanent=is_permanent,
                          product_grade=product_grade,
                          product_stations=product_stations,
                          allowed_ips=allowed_ips,
                          creation_date=creation_date,
                          expiration_date=expiration_date,
    )

    new_license.save()

    return new_license





# def delete_license_data(license_selection):
#     """ Delete license selection from database """
#     print(license_selection)

#     for license_id in license_selection:
#         try:
#             license_data = License.objects.filter(id=license_id).get()
#             entitlement_id = license_data.entitlement_id
#             entitlement_data = Entitlement.objects.filter(id=entitlement_id).get()

#             license_data.delete()
#             entitlement_data.add_license()
        
#         except:
#             return license_id

#     return True


## JS Table Services ##

# def get_license_header():
#     """ Get license table header """
#     license_header = {'id':'ID',
#                     'product_name':'Product',
#                     'version_number':'Version',
#                     'org_name':'Org', 
#                     'host_ip':'Host IP', 
#                     'creator_email': 'Email', 
#                     'is_permanent': 'Permanent',
#                     'product_grade': 'Grade',
#                     'product_stations': 'Stations',
#                     'creation_date': 'Created',
#                     'expiration_date': 'Expires',
#                     }

#     return license_header

