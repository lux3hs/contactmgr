from django import forms

class ChoiceForm(forms.Form):
    """ Form for choosing one of many field options """
    def __init__(self, *args, **kwargs):
        self.field_choices = kwargs.pop('field_choices')
        super(ChoiceForm, self).__init__(*args, **kwargs)
        self.fields["field_choice"] = forms.ChoiceField(choices=self.field_choices, label='')
        self.fields["field_choice"].widget.attrs['class'] = "ChoiceField"

class SearchForm(forms.Form):
    """ Form for searching """
    search_query = forms.CharField(max_length=50, label='')
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields["search_query"].widget.attrs['class'] = "CharField"

class SearchChoiceForm(forms.Form):
    #Set widget fields
    def __init__(self, *args, **kwargs):
        self.choice_list = kwargs.pop('choice_list')
        super(SearchChoiceForm, self).__init__(*args, **kwargs)
        self.fields['search_field'] = forms.CharField(max_length=50, label='')
        self.fields['search_field'].widget.attrs['class'] = "CharField"
        self.fields['choice_field'] = forms.ChoiceField(choices=self.choice_list, label='')
        self.fields['choice_field'].widget.attrs['class'] = "ChoiceField"

class NewLicenseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.product_choices = kwargs.pop('product_choices')
        super(NewLicenseForm, self).__init__(*args, **kwargs)
        self.fields['re_seller'] = forms.CharField(max_length=50)
        self.fields['product_name'] = forms.ChoiceField(choices=self.product_choices)
        self.fields['product_name'].widget.attrs['class'] = "ChoiceField"
        self.fields['host_ip'] = forms.CharField(max_length=50)
        self.fields['is_permanent'] = forms.BooleanField(required=False)
        self.fields["product_grade"] = forms.CharField(max_length=50)
        self.fields["product_stations"] = forms.IntegerField(max_value=999999)
        self.fields["allowed_ips"] = forms.IntegerField(max_value=999999)
        # self.fields['creation_date'] = forms.DateTimeField()
        self.fields['expiration_date'] = forms.DateField()
