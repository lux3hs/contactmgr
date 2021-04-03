import json

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from manage_licenses.views import download_license_package
from .models import Contact, Organization, Product, Entitlement
from .forms import (ContactCreationForm,
                    ContactEditForm,
                    OrgCreationForm,
                    ProductCreationForm,
                    EntitlementCreationForm,
                    EntitlementEditForm,
                    SearchChoiceForm,
                    ChoiceForm)

#Specify method imports
from .services import *

SUPER_ORG = "automai"
SUPER_USER = "superuser"

@login_required
def manage_contacts(request):
    """ Redirect contact based on organization """
    SUPER_ORG_ID = get_superorg_id(SUPER_ORG)
    current_user = request.user
    user_id = current_user.id
    contact_data = Contact.objects.filter(user=user_id).get()
    # org_id = contact_data.organization.id
    # contact_role = contact_data.role

    if contact_data.organization.id == SUPER_ORG_ID:
        return HttpResponseRedirect(reverse('admin_portal'))

    else:
        return HttpResponseRedirect(reverse('client_portal'))


@login_required
def admin_portal(request):
    SUPER_ORG_ID = get_superorg_id(SUPER_ORG)
    current_user = request.user
    user_id = current_user.id
    contact_data = Contact.objects.filter(user=user_id).get()

    # if contact_data.organization.id != SUPER_ORG_ID:
    #     return HttpResponseRedirect(reverse('client_portal'))

    contact_header = get_contact_header()
    contact_choice_list = get_choice_list(contact_header)
    except_list = ["empty_column", "check_box", "delete_button"]
    for choice in contact_choice_list:
        if choice in except_list:
            contact_choice_list.remove(choice)

    contact_search_form = SearchChoiceForm(auto_id='contact_search_form_%s', choice_list=contact_choice_list)

    org_data = Organization.objects.all()
    org_list = []
    for organization in org_data:
        org_list.append((organization.org_name, organization.org_name))

    product_data = Product.objects.all()
    product_list = []
    for product in product_data:
        product_list.append((product.product_name, product.product_name))
        
    if request.method == 'POST':
        entitlement_form = EntitlementCreationForm(request.POST, product_list=product_list, org_list=org_list)
        if entitlement_form.is_valid():
            user_query = request.POST
            success_message = add_new_entitlement(contact_data, user_query)
            messages.add_message(request, messages.INFO, success_message)
            return HttpResponseRedirect(request.path_info)

    else:
        print("form invalid")
        entitlement_form = EntitlementCreationForm(org_list=org_list, product_list=product_list)
    
    
    context = {'contact_data':contact_data,
               'entitlement_form':entitlement_form,
               'contact_search_form':contact_search_form,
            }

    return render(request, "manage_contacts/admin-portal.html", context)


@login_required
def client_portal(request):
    """ Render manage-licenses html page """
    current_user = request.user
    user_id = current_user.id
    contact_data = Contact.objects.filter(user=user_id).get()
    org_id = contact_data.organization.id
    product_entitlements = Entitlement.objects.filter(organization=org_id)
    product_choices = []

    for entitlement in product_entitlements:
        product_choices.append((entitlement.product.product_name, entitlement.product.product_name))
    
    contact_header = get_contact_header()
    contact_choice_list = get_choice_list(contact_header)
    except_list = ["empty_column", "check_box", "delete_button"]
    for choice in contact_choice_list:
        if choice in except_list:
            contact_choice_list.remove(choice)

    contact_search_form = SearchChoiceForm(auto_id='contact_search_form_%s', choice_list=contact_choice_list)

    if request.POST.get("save-license"):
        license_choice_form = ChoiceForm(request.POST, choice_list=product_choices)
        
        if license_choice_form.is_valid():
            user_query = request.POST
            product_choice = user_query.get('choice_field')
            return download_license_package(request, product_choice, product_entitlements)

    else:
        license_choice_form = ChoiceForm(choice_list=product_choices)

    context = {'license_choice_form':license_choice_form, 'contact_data':contact_data, 'contact_search_form':contact_search_form}
    return render(request, "manage_contacts/client-portal.html", context)


@login_required
def edit_entitlement_data(request, query_string):
    """ Edit entitlement fields """
    current_user = request.user
    user_id = current_user.id
    contact_data = Contact.objects.filter(user_id=user_id).get()
    query_data = json.loads(query_string)
    if len(query_data) > 1:
        messages.add_message(request, messages.INFO, 'Too many selected')
        return HttpResponseRedirect(reverse('manage_contacts'))
    
    else:
        entitlement_selection = Entitlement.objects.filter(id=query_data[0]).get()

    org_data = Organization.objects.all()
    org_list = []
    for organization in org_data:
        org_list.append((organization.org_name, organization.org_name))

    product_data = Product.objects.all()
    product_list = []
    for product in product_data:
        product_list.append((product.product_name, product.product_name))
        
    
    if request.method == 'POST':
        edit_entitlement_form = EntitlementEditForm(request.POST, product_list=product_list, org_list=org_list)
        if edit_entitlement_form.is_valid():
            user_query = request.POST
            
            success_message = edit_entitlement(contact_data, entitlement_selection, user_query)
            messages.add_message(request, messages.INFO, success_message)
            return HttpResponseRedirect(request.path_info)

    else:
        edit_entitlement_form = EntitlementEditForm(org_list=org_list, product_list=product_list)


    context = {'contact_data':contact_data, 'entitlement_selection':entitlement_selection, 'edit_entitlement_form':edit_entitlement_form, 'super_org':SUPER_ORG}
    return render(request, "manage_contacts/edit-entitlement.html", context)

@login_required
def get_entitlement_data(request):
    """ Get entitlement data for populating tables """
    current_user = request.user
    user_id = current_user.id
    contact_data = Contact.objects.filter(user=user_id).get()

    if contact_data.organization.org_name == SUPER_ORG:
        entitlement_data = Entitlement.objects.all()
        table_header = get_entitlement_header()

    else:
        entitlement_data = Entitlement.objects.filter(organization=contact_data.organization.id)
        table_header = get_client_ent_header()
    
    table_data = get_table_data(table_header, entitlement_data)
    return JsonResponse(table_data)


@login_required
def delete_entitlement_selection(request, query_string):
    """ Delete entitlement selection on user request """
    entitlement_selection = json.loads(query_string)
    response = delete_entitlement_data(entitlement_selection)
    
    if response is True:
        return get_entitlement_data(request)
        
    else:
        return get_entitlement_data(request)


@login_required
def add_contact(request):
    """ Render add-contact html page """    
    current_user = request.user
    user_id = current_user.id
    contact_data = Contact.objects.filter(user_id=user_id).get()
    contact_data = Contact.objects.filter(user_id=user_id).get()
    org_objects = Organization.objects.all()
    
    choice_list = []
    for org_object in org_objects:
        choice_list.append(org_object.org_name)

    if request.method == 'POST':
        contact_form = ContactCreationForm(request.POST)

        if contact_form.is_valid():
            user_query = request.POST
            if request.POST.get('select_org'):
                org_selection = request.POST.get('select_org')
                new_contact_org = Organization.objects.filter(org_name=org_selection).get()

            else:
                new_contact_org = contact_data.organization

            add_new_contact(user_query=user_query, contact_organization=new_contact_org)
            messages.add_message(request, messages.INFO, 'New contact created')
            return HttpResponseRedirect(request.path_info)

    else:
        contact_form = ContactCreationForm()
        contact_form.order_fields(["contact_role", "contact_status"])

    context = {'contact_data':contact_data, 'contact_form':contact_form, 'choice_list':choice_list, 'super_org':SUPER_ORG}
    return render(request, "manage_contacts/add-contact.html", context)

@login_required
def edit_contact_data(request, query_string):
    """ Edit contact fields """
    query_data = json.loads(query_string)
    if len(query_data) > 1:
        messages.add_message(request, messages.INFO, 'Too many selected')
        return HttpResponseRedirect(reverse('manage_contacts'))

    else:
        contact_selection = Contact.objects.filter(id=query_data[0]).get()
        print(contact_selection)

    current_user_object = request.user
    user_id = current_user_object.id
    current_contact = Contact.objects.filter(user_id=user_id).get()
    # contact_data = Contact.objects.filter(user_id=user_id).get()
    org_objects = Organization.objects.all()
    
    choice_list = []
    for org_object in org_objects:
        choice_list.append(org_object.org_name)

    if request.method == 'POST':
        edit_contact_form = ContactEditForm(request.POST)

        if edit_contact_form.is_valid():
            user_query = request.POST
            if request.POST.get('select_org'):
                org_selection = request.POST.get('select_org')
                new_contact_org = Organization.objects.filter(org_name=org_selection).get()

            else:
                new_contact_org = current_contact.organization

            response = edit_contact(current_user=current_contact, 
                                    user_query=user_query, 
                                    contact_object=contact_selection, 
                                    contact_organization=new_contact_org)
            
            messages.add_message(request, messages.INFO, response)
            return HttpResponseRedirect(request.path_info)

    else:
        edit_contact_form = ContactEditForm()
        edit_contact_form.order_fields(["contact_role", "contact_status"])

    context = {'current_contact':current_contact, 'contact_selection':contact_selection, 'edit_contact_form':edit_contact_form, 'choice_list':choice_list, 'super_org':SUPER_ORG}
    return render(request, "manage_contacts/edit-contact.html", context)

@login_required
def get_contact_data(request):
    """ Provide contact data for populating tables """
    SUPER_ORG_ID = get_superorg_id(SUPER_ORG)

    current_user = request.user
    user_id = current_user.id
    user_data = Contact.objects.filter(user_id=user_id).get()
    org_id = user_data.organization.id
    
    if org_id == SUPER_ORG_ID:
        contact_data = Contact.objects.all()

    else:
        contact_data = Contact.objects.filter(organization=org_id)
    
    table_header = get_contact_header()
    table_data = get_table_data(table_header, contact_data)
    return JsonResponse(table_data)

@login_required
def delete_contact_selection(request, query_string):
    """ Delete contact selection on user request """
    contact_selection = json.loads(query_string)
    current_user = request.user
    user_id = current_user.id
    user_data = Contact.objects.filter(user=user_id).get()

    if user_data.role == "admin":

        response = delete_contact_data(current_user, contact_selection)
        
        if response is True:
            return get_contact_data(request)
        
        else:
            return get_contact_data(request)

    else:
        messages.add_message(request, messages.INFO, "not authorized")
        return HttpResponseRedirect(request.path_info)


@login_required
def add_organization(request):
    """ Render add organization page"""
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
        org_form = OrgCreationForm()


    context = {'user_role':user_role, 'user_org':user_org, 'org_form':org_form}
    return render(request, "manage_contacts/add-organization.html", context)
    
@login_required
def get_org_data(request):
    """ Get org data for populating tables """
    org_data = Organization.objects.all()
    table_header = get_org_header()
    table_data = get_table_data(table_header, org_data)
    return JsonResponse(table_data)

@login_required
def delete_org_selection(request, query_string):
    """ Delete org selection on user request """
    current_user = request.user
    org_selection = json.loads(query_string)
    response = delete_org_data(current_user, org_selection)
    
    if response is True:
        return get_org_data(request)
        
    else:

        return get_org_data(request)


@login_required
def add_product(request):
    """ Render add product page """
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
        product_form = ProductCreationForm()

    context = {'user_role':user_role, 'user_org':user_org, 'product_form':product_form}
    return render(request, "manage_contacts/add-product.html", context)
    
@login_required
def get_product_data(request):
    """ Get product data for populating tables """
    product_data = Product.objects.all()
    table_header = get_product_header()
    table_data = get_table_data(table_header, product_data)
    return JsonResponse(table_data)

@login_required
def delete_product_selection(request, query_string):
    """ Delete product selection on user request """
    product_selection = json.loads(query_string)
    response = delete_product_data(product_selection)
    
    if response is True:
        return get_product_data(request)
        
    else:
        return get_product_data(request)
