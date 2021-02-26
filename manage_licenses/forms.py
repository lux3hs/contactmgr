from django import forms


class ProductForm(forms.Form):
    def __init__(self, *args, **kwargs):
        products = kwargs.pop('products')
        super(ProductForm, self).__init__(*args, **kwargs)
       
        self.fields["product_choice"] = forms.ChoiceField(choices=products, label='')
        self.fields["product_choice"].widget.attrs['class'] = "selectField"

        # Field extension example
    #     self.fields['myField'] = forms.ChoiceField(choices=[('newproduct', 'newproduct')])

    # class Meta:
    #     fields=['myField', 'MyotherField']

class SearchForm(forms.Form):
    product_search = forms.CharField(max_length=50, label='')