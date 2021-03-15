from django import forms
from django.contrib.auth.forms import UserCreationForm


class ContactCreationForm(UserCreationForm):
    #Set widget fields
    contact_firstname = forms.CharField(max_length=50, label="Firstname")
    contact_lastname = forms.CharField(max_length=50, label="Lastname")
    contact_email = forms.EmailField(max_length=50, label="Email")
    role_choices = [('user','user'), ('admin','admin')]
    status_choices = [('active', 'active'), ('removed', 'removed')]
    contact_role = forms.ChoiceField(choices=role_choices, label="Role")
    contact_status = forms.ChoiceField(choices=status_choices, label="Status")
    
    #Extend init function to set widget class
    def __init__(self, *args, **kwargs):
        super(ContactCreationForm, self).__init__(*args, **kwargs)
        
        self.fields["username"].widget.attrs['class'] = "CharField"
        self.fields["password1"].widget.attrs['class'] = "CharField"
        self.fields["password2"].widget.attrs['class'] = "CharField"        
        self.fields["contact_firstname"].widget.attrs['class'] = "CharField"
        self.fields["contact_lastname"].widget.attrs['class'] = "CharField"
        self.fields["contact_email"].widget.attrs['class'] = "CharField"
        self.fields["contact_role"].widget.attrs['class'] = "ChoiceField"
        self.fields["contact_status"].widget.attrs['class'] = "ChoiceField"

    #Validate passwords
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2

class OrgCreationForm(forms.Form):
    ORG_TYPE_CHOICES = [('customer', 'customer'), ('partner', 'partner')]
    org_type = forms.ChoiceField(choices=ORG_TYPE_CHOICES)
    org_name = forms.CharField(max_length=50)
    org_domain = forms.CharField(max_length=50)

class ProductCreationForm(forms.Form):
    product_name = forms.CharField(max_length=50)
    product_version = forms.CharField(max_length=50)


class EntitlementCreationForm(forms.Form):
    max_licenses = forms.IntegerField(max_value=1000)
    def __init__(self, *args, **kwargs):
        self.product_list = kwargs.pop('product_list')
        self.org_list = kwargs.pop('org_list')
        super(EntitlementCreationForm, self).__init__(*args, **kwargs)
        self.fields['product_choice'] = forms.ChoiceField(choices=self.product_list)
        self.fields['org_choice'] = forms.ChoiceField(choices=self.org_list)

 
class SearchChoiceForm(forms.Form):
    #Set widget fields
    choices = [("first_name", "First Name"), ("last_name", "Last Name"), ("email", "Email")]
    search_field = forms.CharField(max_length=50, label='')
    filter_choice = forms.ChoiceField(choices=choices, label='')
    
    #Extend init function to set widget class
    def __init__(self, *args, **kwargs):
        super(SearchChoiceForm, self).__init__(*args, **kwargs)
        self.fields["filter_choice"].widget.attrs['class'] = "ChoiceField"
        self.fields["search_field"].widget.attrs['class'] = "CharField"
