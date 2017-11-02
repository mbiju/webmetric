from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']

        def clean(self):
            cleaned_data = super(OrderCreateForm, self).clean()
            first_name = cleaned_data.get('first_name')
            last_name = cleaned_data.get('last_name')
            email = cleaned_data.get('email')
            address = cleaned_data.get('address')
            postal_code = cleaned_data.get('postal_code')
            city = cleaned_data.get('city')

