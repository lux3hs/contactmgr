from django import forms
from django.contrib.auth.forms import UserCreationForm


class ContactCreationForm(UserCreationForm):
    contact_firstname = forms.CharField(max_length=50, label="Firstname")
    contact_lastname = forms.CharField(max_length=50, label="Lastname")
    contact_email = forms.EmailField(max_length=50, label="Email")
    role_choices = [('user','user'), ('admin','admin')]
    status_choices = [('active', 'active'), ('removed', 'removed')]
    contact_role = forms.ChoiceField(choices=role_choices, label="Role")
    contact_status = forms.ChoiceField(choices=status_choices, label="Status")


    def __init__(self, *args, **kwargs):
        super(ContactCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'contactForm'


            # self.fields["product_choice"].widget.attrs['class'] = "selectField"


    
