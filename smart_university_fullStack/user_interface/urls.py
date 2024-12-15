from django.urls import path,include
from . import views
       
urlpatterns=[
    path('',views.home,name='home'),
    # path('login',include('django.contrib.auth.urls')  )
    path('logout/',views.userLogout,name='logout' ),
    path('register/',views.create_student,name='register'),
    path('login/',views.login_user,name='login'),
    path('student_dashboard/',views.student_dashboard,name='student_dashboard'),
    path('teacher_dashboard/',views.teacher_dashboard,name='teacher_dashboard'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('technical_team_dashboard/',views.technical_team_dashboard,name='technical_team_dashboard'),
    path('control_settings/', views.control_settings, name='control_settings'),
    path('control_settings_react/', views.control_settings_react, name='control_settings_react'),
    path('admin_attandance_dashboard/', views.admin_attandance_dashboard, name='admin_attandance_dashboard'),

]

