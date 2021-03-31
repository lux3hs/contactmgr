import datetime
import os
import os.path

from django.conf import settings
from django.utils.dateparse import parse_date

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


##Keygen services##

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
        os.system(exec_string)
        return key_name

    except: 
        return None


def read_key_file(key_name):
    """ Read file created by AlKeyMaker.exe """
    file_dir = base_dir + "/bin/keygen/" + key_name
    f = open(file_dir, "r")
    key_text = f.read()
    if "Key=" in key_text:
        coded_key = key_text[key_text.index("Key=") + 4 : len(key_text)]

    else:
        coded_key = False

    return coded_key



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

