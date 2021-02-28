from django import forms


class ChoiceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.field_choices = kwargs.pop('field_choices')
        super(ChoiceForm, self).__init__(*args, **kwargs)
       
        self.fields["field_choice"] = forms.ChoiceField(choices=self.field_choices, label='')
        self.fields["field_choice"].widget.attrs['class'] = "ChoiceField"

class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=50, label='')
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        self.fields["search_query"].widget.attrs['class'] = "CharField"
