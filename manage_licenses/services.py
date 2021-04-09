import os
import os.path

import datetime

from django.conf import settings

from .models import License

from manage_contacts.models import Product, Organization

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


def package_master_data(user_query, contact_data, license_data):
    ml_ID = str(license_data.id)
    ml_org_name = str(license_data.org_name)
    print(user_query)
    ml_org_host_IP = str(user_query.get('host_ip' + str(license_data.id))) 
    ml_email = str(contact_data.user.email)
    ml_phone = str(contact_data.phone)

    master_header = ('Master License ID: ' + ml_ID + "\r\n" +
                'Organization Name: ' + ml_org_name + "\r\n" +
                'Organization Host/IP: ' + ml_org_host_IP + "\r\n" +
                'Email Address: ' + ml_email + "\r\n" +
                'Phone Number: ' + ml_phone + "\r\n")

    product_name = license_data.product_name
    product_version = license_data.product_version

    product_stations = str(user_query.get('product_stations'))
    product_grade = str(user_query.get('product_grade'))
    support_id = str(license_data.id)
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

    key_name = "ml_" + str(license_data.id)

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


def add_new_license(contact_data):
    creator_email = contact_data.user.email
    creator_phone = contact_data.phone

    org_name = "automai"
    product_name = "AppLoader"

    product_data = Product.objects.filter(product_name=product_name).get()
    product_version = product_data.product_version
    product_grade = product_data.product_grade
    
    max_licenses = 100
    total_licenses = 100
    
    re_seller = ""
    host_ip = ""
    is_permanent = False
    product_stations = 1
    allowed_ips = 0

    creation_date = datetime.datetime.now().replace(microsecond=0)
    time_change = datetime.timedelta(weeks=2)
    expiration_date = creation_date + time_change

    new_license = License(org_name=org_name,
                          product_name=product_name,
                          product_version=product_version,
                          creator_email=creator_email,
                          creator_phone=creator_phone,
                          max_licenses=max_licenses,
                          total_licenses=total_licenses,
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


def update_license_data (user_query, is_client=False):
    license_id = user_query.get('license-radio-button')
    license_data = License.objects.filter(id=license_id).get()

    id_string = str(license_id)

    if is_client:
        host_ip = user_query.get('host_ip' + id_string)
        if host_ip:
            license_data.host_ip = host_ip
        license_data.save()

        return license_data

    product_name = user_query.get('product_name' + id_string)
    if product_name:
        product_object = Product.objects.filter(product_name=product_name).get()
        product_version = product_object.product_version
        license_data.product_name = product_name
        license_data.product_version = product_version

    org_id = user_query.get('org_id' + id_string)
    if org_id:
        org_data = Organization.objects.filter(id=org_id).get()
        org_name = org_data.org_name
        license_data.org_name = org_name
    
    max_licenses = user_query.get('max_licenses' + id_string)
    if max_licenses:
        license_data.max_licenses = int(max_licenses)
        total_licenses = max_licenses
        license_data.total_licenses = int(total_licenses)

    host_ip = user_query.get('host_ip' + id_string)
    if host_ip:
        license_data.host_ip = host_ip

    product_stations = user_query.get("product_stations" + id_string)
    if product_stations:
        license_data.product_stations = product_stations
    
    allowed_ips = user_query.get('allowed_ips' + id_string)
    if allowed_ips:
        license_data.allowed_ips = int(allowed_ips)

    re_seller = user_query.get('re_seller' + id_string)
    if re_seller:
        license_data.re_seller = re_seller

    is_permanent = user_query.get('is_permanent' + id_string)
    if is_permanent:
        license_data.is_permanent = True

    elif is_permanent:
        license_data.is_permanent = False

    is_master = user_query.get('is_master' + id_string)

    if is_master:
        license_data.is_master = True

    else:
        license_data.is_master = False

    expiration_date = user_query.get('expiration_date' + id_string)
    if expiration_date:
        current_date = datetime.datetime.now().replace(microsecond=0)

        date_time_obj = datetime.datetime.strptime(expiration_date, '%Y-%m-%d')

        expiration_datetime = datetime.datetime.combine(date_time_obj.date(), current_date.time())
        license_data.expiration_date = expiration_datetime


    license_data.save()

    return license_data


def delete_license_data(license_selection):
    """ Delete license selection from database """
    for license_id in license_selection:
        try:
            license_data = License.objects.filter(id=license_id).get()
            license_data.delete()

            return True
        
        except:
            return license_id

    
## JS Table Services ##

def get_license_table_header():
    """ Get license table header """
    license_header = {'radio_button': '',
                      'empty_column':"<pre>    </pre>",
                      'org_name_widget':'Org',
                      'product_name_widget':'Product',
                      'total_licenses_widget':'Total',
                      'max_licenses_widget':'Max',
                      'host_ip_widget':'Host IP',
                      'product_stations_widget':'Stations',
                      'is_master_widget':'Master',
                      'is_permanent_widget':'Permanent',
                      'expiration_date_widget':'Expires',
                      'delete_button':'',

                    }

    return license_header

def get_client_license_table_header():
    license_header = {'radio_button': '',
                      'org_name':'Org',
                      'product_name':'Product',
                      'product_version':'Version',
                      'num_allocated':'Allocated',
                      'host_ip_widget':'Host IP',
                      'is_permanent': 'Permanent',
                      'product_stations': 'Stations',
                      'creation_date': 'Created',
                      'expiration_date': 'Expires',
                    }

    return license_header


