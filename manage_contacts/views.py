import datetime

from django.contrib.auth.models import User

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import Contact, Organization, Product, Entitlement
from .forms import ContactCreationForm, SearchChoiceForm, OrgCreationForm, ProductCreationForm, EntitlementCreationForm

from .services import *


# Create your views here.

@login_required
def manage_contacts(request):
    """ Render manage-contacts html page """
    #Get current user info
    current_user = request.user
    user_id = current_user.id
    user_email = current_user.email
    user_data = Contact.objects.filter(user_id=user_id).get()
    user_role = user_data.role
    user_org = user_data.organization.org_name
    org_id = user_data.organization.id
    
    #Get list of users by current contact's organization
    user_objects = User.objects
    contact_objects = Contact.objects.filter(organization=org_id)
    
    #Create a list of contact information to display in table
    contact_list = []
    for contact in contact_objects:
        user_dict = {}
        user_id = contact.user.id
        user = user_objects.filter(id=user_id).get()
        user_dict["first_name"] = user.first_name
        user_dict["last_name"] = user.last_name
        user_dict["email"] = user.email
        user_dict["contact_id"] = contact.id
        user_dict["role"] = contact.role
        user_dict["status"] = contact.status
        user_dict["org_id"] = contact.organization.id
        user_dict["user_org"] = contact.organization.org_name
        contact_list.append(user_dict)

    #Create a form for filtering contacts
    filter_form = SearchChoiceForm()

    if request.GET.get("filter_choice"):
        user_query = request.GET
        filter_choice = user_query.get("filter_choice")
        search_field = user_query.get("search_field")
        temp_list = []
        for contact in contact_list:
            if search_field.lower() in contact[filter_choice].lower():
                temp_list.append(contact)

        contact_list = temp_list

    #Clear search filter on response from clear search button
    elif request.GET.get("clear_search"):
        return HttpResponseRedirect(request.path_info)

    #Check for input from delete contacts
    if request.GET.get('delete_contact_selection'):
        print("hello")
        user_selection = request.GET.getlist("contact_selection")
        delete_contacts(current_user, user_selection)
        messages.add_message(request, messages.INFO, 'Selection Deleted')
        return HttpResponseRedirect(request.path_info)

    #Render variables in html
    context = {'user_email':user_email,
               'user_role':user_role,
               'org_id':org_id,
               'user_org':user_org,
               'contact_list':contact_list,
               'filter_form':filter_form
            }

    return render(request, "manage_contacts/manage-contacts.html", context)

@login_required
def add_contact(request):
    """ Render add-contact html page """
    #Get current contact role to check for admin access
    current_user = request.user
    user_id = current_user.id
    user_data = Contact.objects.filter(user_id=user_id).get()
    user_role = user_data.role

    #Check for user submission
    if request.method == 'POST':
        contact_form = ContactCreationForm(request.POST)

        if contact_form.is_valid():
            #Get submission data
            user_query = request.POST
            contact_username = user_query.get('username')
            password1 = user_query.get('password1')
            contact_firstname = user_query.get('contact_firstname')
            contact_lastname = user_query.get('contact_lastname')
            contact_email = user_query.get('contact_email')
            contact_role = user_query.get('contact_role')
            contact_status = user_query.get('contact_status')
            # contact_phone = user_query.get('contact_phone')

            #Get current contact organization
            contact_data = Contact.objects.filter(user_id=user_id).get()
            contact_organization = contact_data.organization

            #Create user
            user = User.objects.create_user(contact_username, contact_email, password1)
            user.first_name = contact_firstname
            user.last_name = contact_lastname
            user.save()

            #Create contact
            new_contact = Contact(creation_date=datetime.datetime.now(),
                                role=contact_role,
                                status=contact_status,
                                organization=contact_organization,
                                user=user)
            new_contact.save()
            
            messages.add_message(request, messages.INFO, 'New contact created')
            return HttpResponseRedirect(request.path_info)


    else:
        #Create a contact form if no data has been posted
        contact_form = ContactCreationForm()


    #Render variables in html
    context = {'user_role':user_role, 'contact_form':contact_form}
    return render(request, "manage_contacts/add-contact.html", context)

@login_required
def admin_dash(request):
    current_user = request.user
    user_id = current_user.id
    user_data = Contact.objects.filter(user_id=user_id).get()
    user_role = user_data.role
    user_org = user_data.organization.org_name
    context = {'user_role':user_role, 'user_org':user_org}
    return render(request, "manage_contacts/admin-dash.html", context)

@login_required
def add_organization(request):
    org_form = OrgCreationForm()
    current_user = request.user
    user_id = current_user.id
    user_data = Contact.objects.filter(user_id=user_id).get()
    user_role = user_data.role
    user_org = user_data.organization.org_name

    if request.method == 'POST':
        org_form = OrgCreationForm(request.POST)
        if org_form.is_valid():
            user_query = request.POST     

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

                messages.add_message(request, messages.INFO, 'New organization created')
                return HttpResponseRedirect(request.path_info)

            else:
                messages.add_message(request, messages.INFO, 'Organization exists')
                return HttpResponseRedirect(request.path_info)




        else:
            print("invalid")


    context = {'user_role':user_role, 'user_org':user_org, 'org_form':org_form}
    return render(request, "manage_contacts/add-organization.html", context)
    
@login_required
def add_product(request):
    product_form = ProductCreationForm()
    current_user = request.user
    user_id = current_user.id
    user_data = Contact.objects.filter(user_id=user_id).get()
    user_role = user_data.role
    user_org = user_data.organization.org_name

    if request.method == 'POST':
        product_form = ProductCreationForm(request.POST)
        if product_form.is_valid():
            user_query = request.POST

            product_name = user_query.get('product_name')
            product_version = user_query.get('product_version')

            product_data = Product.objects.all()

            product_names = []
            for product in product_data:
                product_names.append(product.product_name)

            if product_name not in product_names:
                new_product = Product(product_name=product_name, product_version=product_version)
                new_product.save()

                messages.add_message(request, messages.INFO, 'New product created')
                return HttpResponseRedirect(request.path_info)

            else:
                messages.add_message(request, messages.INFO, 'Product exists')
                return HttpResponseRedirect(request.path_info)



    context = {'user_role':user_role, 'user_org':user_org, 'product_form':product_form}
    return render(request, "manage_contacts/add-product.html", context)
    
@login_required
def add_entitlement(request):
    current_user = request.user
    user_id = current_user.id
    user_data = Contact.objects.filter(user_id=user_id).get()
    user_role = user_data.role
    user_org = user_data.organization.org_name

    org_data = Organization.objects.all()
    org_list = []
    for organization in org_data:
        org_list.append((organization.org_name, organization.org_name))

    product_data = Product.objects.all()
    product_list = []
    for product in product_data:
        product_list.append((product.product_name, product.product_name))
        
    entitlement_form = EntitlementCreationForm(org_list=org_list, product_list=product_list)
    if request.method == 'POST':
        entitlement_form = EntitlementCreationForm(request.POST, product_list=product_list, org_list=org_list)
        if entitlement_form.is_valid():
            user_query = request.POST

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

                messages.add_message(request, messages.INFO, 'New entitlement created')
                return HttpResponseRedirect(request.path_info)

            else:
                messages.add_message(request, messages.INFO, 'Entitlement exists')
                return HttpResponseRedirect(request.path_info)


    context = {'user_role':user_role, 'user_org':user_org, 'entitlement_form':entitlement_form}
    return render(request, "manage_contacts/add-entitlement.html", context)

