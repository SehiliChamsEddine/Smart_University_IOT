from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('user_interface.urls')),
    path('',include('users.urls')),
    path('',include('data_collect.urls')),
    path('api/',include('api.urls'))
]
