from .models import Contact, Organization


def delete_contacts(current_user, user_selection):
    for contact_id in user_selection:
        user_id = current_user.id
        contact_data = Contact.objects.filter(user=user_id).get()
        contact_org = contact_data.get_contact_org()
        org_id = contact_org.id
        org_contacts = Contact.objects.filter(organization=org_id)
        
        contact_selection = org_contacts.filter(id=contact_id)
        
        contact_selection.delete()