
import datetime

from django.contrib.auth.models import User
from .models import Contact, Organization, Product, Entitlement

def add_new_contact(user_query, contact_organization):
    contact_username = user_query.get('username')
    password1 = user_query.get('password1')
    contact_firstname = user_query.get('contact_firstname')
    contact_lastname = user_query.get('contact_lastname')
    contact_email = user_query.get('contact_email')
    contact_role = user_query.get('contact_role')
    contact_status = user_query.get('contact_status')
    # contact_phone = user_query.get('contact_phone')

    #Create user
    user = User.objects.create_user(contact_username, contact_email, password1)
    user.first_name = contact_firstname
    user.last_name = contact_lastname
    user.save()

    #Update contact that was created on user creation
    new_contact = Contact.objects.filter(user=user).get()
    new_contact.creation_date = datetime.datetime.now()
    new_contact.role = contact_role
    new_contact.status = contact_status
    new_contact.organization = contact_organization
    new_contact.save()

    return new_contact

def delete_contact(user_id):
    if user_id:
        try:
            contact_data = Contact.objects.filter(id=user_id)
            contact_data.delete()
            
            return True

        except:
            return "error"

    else:
        return "no contacts selected"





def delete_org_data(org_selection):
    except_list = ['automai']
    print("orgs:" + str(org_selection))
    try:
        for org_id in org_selection:
            org_data = Organization.objects.filter(id=int(org_id)).get()
            if org_data.org_name in except_list:
                pass
            
            else:      
                org_data.delete()
                return True

    except:
        return org_id


        
def delete_product_data(product_selection):
    try:
        for product_id in product_selection:
            product_data = Product.objects.filter(id=int(product_id)).get()
            product_data.delete()
            return True

    except:
        return product_id


def delete_entitlement_data(entitlement_selection):
    try:
        for ent_id in entitlement_selection:
            ent_data = Entitlement.objects.filter(id=int(ent_id)).get()
            ent_data.delete()
            return True

    except:
        return ent_id



def add_new_organization(user_query):
    org_type = user_query.get('org_type')
    org_name = user_query.get('org_name')
    org_domain = user_query.get('org_domain')
    org_data = Organization.objects.all()
    org_names = []
    for org in org_data:
        org_names.append(org.org_name)

    if org_name not in org_names:
        new_org = Organization(org_type=org_type, org_name=org_name, domain=org_domain)
        new_org.save()

        success_message = "New organization created successfully"

    else: 
        success_message = "Organization exists"

    return success_message

def add_new_product(user_query):
    product_name = user_query.get('product_name')
    product_version = user_query.get('product_version')
    product_data = Product.objects.all()
    product_names = []
    for product in product_data:
        product_names.append(product.product_name)

    if product_name not in product_names:
        new_product = Product(product_name=product_name, product_version=product_version)
        new_product.save()

        success_message = "New product created successfully"

    else: 
        success_message = "Product exists"

    return success_message


def add_new_entitlement(user_query):
    product_choice = user_query.get('product_choice')
    org_choice = user_query.get('org_choice')
    max_licenses = user_query.get('max_licenses')
    total_licenses = max_licenses

    product_object = Product.objects.filter(product_name=product_choice).get()
    org_object = Organization.objects.filter(org_name=org_choice).get()

    entitlement_data = Entitlement.objects.all()
    entitlement_names = []
    for entitlement in entitlement_data:
        entitlement_names.append(entitlement.get_entitlement_name())

    dup_check = org_object.org_name + '/' + product_object.product_name
    
    if dup_check not in entitlement_names:
        new_entitlement = Entitlement(product=product_object, 
                                    organization=org_object, 
                                    max_licenses=max_licenses, 
                                    total_licenses=total_licenses)

        new_entitlement.save()

        success_message = "New entitlement created successfully"

    else: 
        success_message = "Entitlement exists"

    return success_message




# def filter_contacts(contact_list, filter_choice, search_field):
#     filter_list = []
#     for contact in contact_list:
#         if search_field.lower() in contact[filter_choice].lower():
#             filter_list.append(contact)

#     return filter_list


# def delete_object_selection(data_objects, user_selection):
#     for object_id in user_selection:
#         object_selection = data_objects.objects.filter(id=object_id)
#         object_selection.delete()


def get_model_fields(model):
    return model._meta.fields

def get_model_choices(model_fields):
    choice_list = []
    for field in model_fields:
        choice_list.append((field.name, field.name))

    return choice_list


#Requires data table to have gat table dictionary function
def get_table_data(table_header, object_data):
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
            data['success'] = True

        except:
            data['success'] = False

    return data


def get_contact_header():
    contact_header = {'username':'User',
                      'first_name':'First Name',
                      'last_name':'Last Name',
                      'email':'Email',
                      'role':'Role',
                      'status':'Status',
                      'org_name':'Organization',
                    }

    return contact_header



def get_org_header():
    org_header = {"org_type":"Type",
                  "org_name":"Name",
                  "domain":"Domain",
                }

    return org_header

def get_product_header():
    product_header = {'product_name':'Product',
                      'product_version':'Version',
                        }

    return product_header

def get_entitlement_header():
    entitlement_header = {"product_name":"Product",
                          "product_version":"Version",
                          "max_licenses":"Max",
                          "total_licenses":"Total",
                          "num_allocated":"Num Allocated",
    }
    return entitlement_header

def get_choice_list(model_header):
    choice_list = []
    for key in model_header:
        choice_list.append((key, model_header[key]))

    return choice_list