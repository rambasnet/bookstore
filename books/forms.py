from django.contrib import auth
from django import forms
from . import models

class AccountForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password',
                                widget=forms.PasswordInput)
    class Meta:
        model = auth.models.User
        fields = ('first_name', 'last_name', 'username', 'password')

    # can provide clean_<fieldName> to any form field to order to clean the value or 
    # raise form validation error for the specific field
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = auth.models.User
        fields = ['first_name', 'last_name', 'email']
    

class ProfileEditForm(forms.ModelForm):
    dob = forms.DateField(label="Date of birth", 
                        widget=forms.DateInput(attrs={'type': 'date'}, format='%m/%d/%Y'))
    class Meta:
        model = models.Profile
        fields = ['dob', 'photo']
