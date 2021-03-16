import datetime

from django.contrib.auth.models import User

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import Contact, Organization, Product, Entitlement
from .forms import ContactCreationForm, SearchChoiceForm, OrgCreationForm, ProductCreationForm, EntitlementCreationForm

from .services import *


#Manage Contacts Views#
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
    # user_objects = User.objects
    contact_objects = Contact.objects.filter(organization=org_id)
    
    #Create a list of contact information to display in table
    contact_list = []
    for contact in contact_objects:
        user_dict = contact.get_contact_dict()
        contact_list.append(user_dict)

    #Create a form for filtering contacts
    filter_form = SearchChoiceForm()

    if request.GET.get("filter_choice"):
        user_query = request.GET
        filter_choice = user_query.get("filter_choice")
        search_field = user_query.get("search_field")
        contact_list = filter_contacts(contact_list=contact_list, filter_choice=filter_choice, search_field=search_field)

    #Clear search filter on response from clear search button
    elif request.GET.get("clear_search"):
        contact_list = []
        for contact in contact_objects:
            user_dict = contact.get_contact_dict()
            contact_list.append(user_dict)

    #Check for input from delete contacts
    if request.GET.get('delete_contact_selection'):
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

    #Get current contact organization
    contact_data = Contact.objects.filter(user_id=user_id).get()
    contact_organization = contact_data.organization

    #Check for user submission
    if request.method == 'POST':
        contact_form = ContactCreationForm(request.POST)

        if contact_form.is_valid():
            user_query = request.POST
            add_new_contact(user_query=user_query, contact_organization=contact_organization)
            messages.add_message(request, messages.INFO, 'New contact created')
            return HttpResponseRedirect(request.path_info)


    else:
        #Create a contact form if no data has been posted
        contact_form = ContactCreationForm()


    #Render variables in html
    context = {'user_role':user_role, 'contact_form':contact_form}
    return render(request, "manage_contacts/add-contact.html", context)




##Automai admin views
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
            success_message = add_new_organization(user_query)            
            messages.add_message(request, messages.INFO, success_message)
            return HttpResponseRedirect(request.path_info)

        else:
            messages.add_message(request, messages.INFO, "Invalid submission")
            return HttpResponseRedirect(request.path_info)

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
            success_message = add_new_product(user_query)

            messages.add_message(request, messages.INFO, success_message)
            return HttpResponseRedirect(request.path_info)

        else:
            messages.add_message(request, messages.INFO, "Invalid submission")
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
            success_message = add_new_entitlement(user_query)
            messages.add_message(request, messages.INFO, success_message)
            return HttpResponseRedirect(request.path_info)

        else:
            messages.add_message(request, messages.INFO, "Invalid submission")
            return HttpResponseRedirect(request.path_info)

    context = {'user_role':user_role, 'user_org':user_org, 'entitlement_form':entitlement_form}
    return render(request, "manage_contacts/add-entitlement.html", context)

