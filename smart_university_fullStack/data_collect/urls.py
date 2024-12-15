from django.urls import path
from . import views
       
urlpatterns=[
    path('get_latest_data/', views.get_latest_data),
]

