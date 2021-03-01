import datetime

from django.contrib.auth.models import User

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import Contact
from .forms import ContactCreationForm, SearchChoiceForm

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
def edit_contact(request):
    context = {}
    return render(request, "manage_contacts/edit-contact.html", context)

