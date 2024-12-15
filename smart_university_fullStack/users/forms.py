from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser  # Import your CustomUser model
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)
    role = forms.ChoiceField(choices=CustomUser.Role.choices)  # Add role field to the form

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True, is_active=True, is_superuser=False, is_staff=False):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']  # Assign the role from form data
        user.is_active = is_active
        user.is_superuser = is_superuser
        user.is_staff = is_staff
        if commit:
            user.save()
        return user
    

# class SuperUserRegistrationForm(UserCreationForm):
#     email = forms.EmailField(help_text='A valid email address, please.', required=True)
#     role = forms.ChoiceField(choices=CustomUser.Role.choices)  # Add role field to the form

#     class Meta:
#         model = get_user_model()
#         fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

#     def save(self, commit=True):
#         user = super(UserRegistrationForm, self).save(commit=False)
#         # user.
#         user.email = self.cleaned_data['email']
#         user.role = self.cleaned_data['role']  # Assign the role from form data
#         if commit:
#             user.save()
#         return user