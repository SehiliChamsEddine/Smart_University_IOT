from django.urls import path
from .views import ControlSettingsView

urlpatterns = [
    # Your other URL patterns here
    path('control-settings/', ControlSettingsView.as_view(), name='control_settings_api'),
]
