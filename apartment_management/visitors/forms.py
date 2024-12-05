from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Visitor
from django.contrib.auth.models import User, Group

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['name', 'apartment_number', 'check_in', 'check_out']



class ResidentRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
            resident_group = Group.objects.get(name='Resident')  # Ensure "Resident" group exists
            user.groups.add(resident_group)  # Assign the user to the Resident group
        return user



class ReceptionistRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
            receptionist_group = Group.objects.get(name='Receptionist')  # Ensure "Receptionist" group exists
            user.groups.add(receptionist_group)  # Assign the user to the Receptionist group
        return user

