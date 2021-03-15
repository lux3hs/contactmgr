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

class NewLicenseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.product_choices = kwargs.pop('product_choices')
        super(NewLicenseForm, self).__init__(*args, **kwargs)
        self.fields['product_choice'] = forms.ChoiceField(choices=self.product_choices)
        self.fields['product_choice'].widget.attrs['class'] = "ChoiceField"
        self.fields['ip_host'] = forms.CharField(max_length=50)
        self.fields['is_permanent'] = forms.BooleanField(required=False)

        self.fields['creation_date'] = forms.DateTimeField()
        self.fields['expiration_date'] = forms.DateTimeField()