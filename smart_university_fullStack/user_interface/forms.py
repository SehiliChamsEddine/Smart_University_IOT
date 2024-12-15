from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime,AdminTimeWidget

from django.forms.widgets import TimeInput,DateTimeInput

from .models import Student,SetSession
from data_collect.models import *


class CustomDateTimeWidget(DateTimeInput):
    input_type = 'datetime-local'

class SetSessionForm(forms.ModelForm):
    class Meta:
        model = SetSession
        fields = '__all__'

    # Use the custom date and time widget for the time field
    time = forms.DateTimeField(widget=CustomDateTimeWidget(attrs={'format': f'%Y-%m-%dT%H:%M'}))

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['id_number', 'contact_phone', 'group_number']
    password = forms.CharField(widget=forms.PasswordInput)

class ControlSettingsFormPublish(forms.ModelForm):
    class Meta:
        model = ControlSettingsPublish
        fields = ['water_pump_status', 'block1_status', 'block2_status', 'block3_status']
class ControlSettingsForm(forms.ModelForm):
    class Meta:
        model = ControlSettingsRecive
        fields = ['water_pump_status', 'block1_status', 'block2_status', 'block3_status','fire_detection','gas_detection']