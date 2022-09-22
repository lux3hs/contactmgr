from django import forms
from django.contrib.auth.forms import UserCreationForm


class ContactCreationForm(UserCreationForm):
    #Set widget fields
    role_choices = [('user','user'), ('admin','admin')]
    contact_role = forms.ChoiceField(choices=role_choices, label="Role")
    status_choices = [('active', 'active'), ('removed', 'removed')]
    contact_status = forms.ChoiceField(choices=status_choices, label="Status")
    contact_firstname = forms.CharField(max_length=50, label="Firstname")
    contact_lastname = forms.CharField(max_length=50, label="Lastname")
    contact_email = forms.EmailField(max_length=50, label="Email")
    
    
    #Extend init function to set widget class
    def __init__(self, *args, **kwargs):
        super(ContactCreationForm, self).__init__(*args, **kwargs)
        self.fields["contact_role"].widget.attrs['class'] = "ChoiceField"
        self.fields["contact_status"].widget.attrs['class'] = "ChoiceField"
        self.fields["username"].widget.attrs['class'] = "CharField"
        self.fields['username'].help_text = ""
        self.fields["password1"].widget.attrs['class'] = "CharField"
        self.fields["password1"].help_text = ""
        self.fields["password2"].widget.attrs['class'] = "CharField"
        self.fields["password2"].help_text = ""
        self.fields["password2"].label = "Confirmation:"    
        self.fields["contact_firstname"].widget.attrs['class'] = "CharField"
        self.fields["contact_lastname"].widget.attrs['class'] = "CharField"
        self.fields["contact_email"].widget.attrs['class'] = "CharField"

    #Validate passwords
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2
        

class ContactEditForm(forms.Form):
    #Set widget fields
    role_choices = [('user','user'), ('admin','admin')]
    contact_role = forms.ChoiceField(choices=role_choices, label="Role", required=False)
    status_choices = [('active', 'active'), ('removed', 'removed')]
    contact_status = forms.ChoiceField(choices=status_choices, label="Status", required=False)
    contact_firstname = forms.CharField(max_length=50, label="Firstname", required=False)
    contact_lastname = forms.CharField(max_length=50, label="Lastname", required=False)
    contact_email = forms.EmailField(max_length=50, label="Email", required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=True)
    
    #Extend init function to set widget class
    def __init__(self, *args, **kwargs):
        super(ContactEditForm, self).__init__(*args, **kwargs)
        self.fields["contact_role"].widget.attrs['class'] = "ChoiceField"
        self.fields["contact_status"].widget.attrs['class'] = "ChoiceField"
        # self.fields["username"].widget.attrs['class'] = "CharField"
        # self.fields['username'].help_text = ""
        self.fields["password1"].widget.attrs['class'] = "CharField"
        # self.fields["password1"].help_text = ""
        self.fields["password2"].widget.attrs['class'] = "CharField"
        # self.fields["password2"].help_text = ""
        # self.fields["password2"].label = "Confirmation:"    
        self.fields["contact_firstname"].widget.attrs['class'] = "CharField"
        self.fields["contact_lastname"].widget.attrs['class'] = "CharField"
        self.fields["contact_email"].widget.attrs['class'] = "CharField"

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
    def __init__(self, *args, **kwargs):
        super(OrgCreationForm, self).__init__(*args, **kwargs)
        self.fields["org_type"].widget.attrs['class'] = "ChoiceField"

class OrgEditForm(forms.Form):
    ORG_TYPE_CHOICES = [('customer', 'customer'), ('partner', 'partner')]
    org_type = forms.ChoiceField(choices=ORG_TYPE_CHOICES, required=False)
    org_name = forms.CharField(max_length=50, required=False)
    org_domain = forms.CharField(max_length=50, required=False)
    def __init__(self, *args, **kwargs):
        super(OrgEditForm, self).__init__(*args, **kwargs)
        self.fields["org_type"].widget.attrs['class'] = "ChoiceField"

class ProductCreationForm(forms.Form):
    product_name = forms.CharField(max_length=50)
    product_version = forms.CharField(max_length=50)
    GRADE_CHOICES = [('standard', 'standard'), ('enterprise', 'enterprise')]
    product_grade = forms.ChoiceField(choices=GRADE_CHOICES)

class ProductEditForm(forms.Form):
    product_name = forms.CharField(max_length=50, required=False)
    product_version = forms.CharField(max_length=50, required=False)
    GRADE_CHOICES = [('standard', 'standard'), ('enterprise', 'enterprise')]
    product_grade = forms.ChoiceField(choices=GRADE_CHOICES)


class SearchForm(forms.Form):
    """ Form for searching """
    search_query = forms.CharField(max_length=50, label='')
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields["search_query"].widget.attrs['class'] = "CharField"

class ChoiceForm(forms.Form):
    #Set widget fields
    def __init__(self, *args, **kwargs):
        self.choice_list = kwargs.pop('choice_list')
        super(ChoiceForm, self).__init__(*args, **kwargs)
        self.fields['choice_field'] = forms.ChoiceField(choices=self.choice_list)
        self.fields['choice_field'].widget.attrs['class'] = "ChoiceField"

class SearchChoiceForm(forms.Form):
    #Set widget fields
    def __init__(self, *args, **kwargs):
        self.choice_list = kwargs.pop('choice_list')
        super(SearchChoiceForm, self).__init__(*args, **kwargs)
        self.fields['search_field'] = forms.CharField(max_length=50, label='')
        self.fields['search_field'].widget.attrs['class'] = "CharField"
        self.fields['choice_field'] = forms.ChoiceField(choices=self.choice_list, label='')
        self.fields['choice_field'].widget.attrs['class'] = "ChoiceField"

