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
