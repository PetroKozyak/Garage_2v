from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import requests


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return first_name.title()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        return last_name.title()

    def clean_email(self):
        value = self.cleaned_data.get('email', '')
        if len(value) > 0:
            resp = requests.get('https://api.mailgun.net/v2/address/validate',
                                params={'api_key': 'pubkey-7049tobos-x721ipc8b3dp68qzxo3ri5', 'address': value}).json()

            if not resp.get('is_valid', False) or resp.get("parts").get('domain') != "softonix.org":
                msg = ('Invalid email address.')
                if resp.get('did_you_mean'):
                    msg = msg + ' ' + ('Did you mean:') + resp.get('did_you_mean')
                raise forms.ValidationError(msg, code='invalid_email')
        return value
