from django.shortcuts import redirect
from django.http import HttpResponse
from functools import wraps


def notLoggedUsers(view_func):
    def wrapper_func(request , *args,**kwargs):
        if request.user.is_authenticated:
            if request.user.role == 'ADMIN':
                return redirect('admin_dashboard')
            elif request.user.role == 'TEACHER':
                return redirect('teacher_dashboard')
            elif request.user.role == 'STUDENT':
                return redirect('student_dashboard')
            elif request.user.role == 'TECHNICAL_TEAM':
                return redirect('technical_team_dashboard')
        else:
            return view_func(request , *args,**kwargs)
    return wrapper_func


def notLoggedUsers1(view_func):
    def wrapper_func(request , *args,**kwargs):
        if request.user.is_authenticated:
            return redirect('teachers_dashboard')
        else:
            return view_func(request , *args,**kwargs)
    return wrapper_func


def notLoggedUsers2(view_func):
    def wrapper_func(request , *args,**kwargs):
        if request.user.is_authenticated:
            return redirect('admin_dashboard')
        else:
            return view_func(request , *args,**kwargs)
    return wrapper_func





def allowedUsers(allowedGroups=[]):
    def decorator(view_func):
        def wrapper_func(request , *args,**kwargs): 
            group = None
            if request.user.groups.exists():
               group =  request.user.groups.all()[0].name
            if group in allowedGroups:
               return view_func(request , *args,**kwargs)
            else:
                return redirect('user_profile')
            
        return wrapper_func
    return decorator




def forAdmins(view_func): 
        def wrapper_func(request , *args,**kwargs): 
            group = None
            if request.user.groups.exists():
               group =  request.user.groups.all()[0].name
            if group == 'admin':
               return view_func(request , *args,**kwargs)
            if group == 'customer':
                return redirect('user_profile')
            
        return wrapper_func 



def forAdmins(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.role == 'ADMIN':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login_student')  # Redirect to login page for non-admin users
    return wrapper