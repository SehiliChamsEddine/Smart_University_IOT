from django.contrib import admin
from.models import *
from .forms import SetSessionForm
# Register your models here.

admin.site.register(Student)

admin.site.register(TechnicalTeam)
admin.site.register(Teacher)
admin.site.register(Administration)
admin.site.register(Attendance)
admin.site.register(GR_number)

class SetSessionAdmin(admin.ModelAdmin):
    form = SetSessionForm  # Use the custom form for SetSession

# Register the SetSession model with the custom admin class
admin.site.register(SetSession, SetSessionAdmin)


