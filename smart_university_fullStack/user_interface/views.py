from django.shortcuts import render, redirect
import time 
# from .anti_spoofing.test  import test 
from django.http import JsonResponse
from .forms import *
from .models import *
from data_collect.models import *
from django.contrib.auth import authenticate, login ,logout       
from django.shortcuts import render, redirect          
from django.contrib.auth.decorators import  login_required
from .decorators import notLoggedUsers , forAdmins
from users.forms import UserRegistrationForm
def home(request):   
    return render(request,'AI/visitors_page/index.html')

#    ------------------------------------------ student dash board -----------------
@login_required(login_url='login_student')
def student_dashboard(request):
    if request.user.role != 'STUDENT':
        return redirect('login_student')
    # Get the student object for the logged-in user
    student = Student.objects.get(user=request.user)
    # Get the attendance objects for the student
    attendance_objects = Attendance.objects.filter(student=student)
    # Create a list to store attendance information for rendering in the template
    attendance_info = []
    # Loop through the attendance objects
    user_info = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }
    for attendance in attendance_objects:
        session_info = {
            'time': attendance.session.time,
            'class_name': attendance.session.class_name,
            'group': attendance.session.group.group_name,
            'teacher': f'{attendance.session.teacher.user.first_name} {attendance.session.teacher.user.last_name}',
            'module': attendance.session.teacher.module,
        }
        attendance_info.append(session_info)

    return render(request, 'AI/students/dashboard_students.html', {'attendance_info': attendance_info,'user_info':user_info})

#    ------------------------------------------- teacher dashboard -----------------

@login_required(login_url='login_student')
def teacher_dashboard(request):
    if request.user.role != 'TEACHER':
        return redirect('login')

    # Get the teacher object for the logged-in user
    teacher = Teacher.objects.get(user=request.user)
     # Find all sessions that contain this teacher
    groups = GR_number.objects.all()
    sessions_taught = SetSession.objects.filter(teacher=teacher)
    # Get the teacher's sessions
    teacher_attandance = Attendance.objects.filter(teacher=teacher)

    # Create a list to store session information for rendering in the template
    session_teacher_info = []
    session_students_info = []
    user_info={
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }
    # Loop through the teacher's sessions
    for attendance in teacher_attandance:
        session_data = {
            'group': attendance.session.group.group_name,
            'student_name':attendance.session.group.group_name,
            'class_name': attendance.session.class_name,
            'module': teacher.module,
            'time': attendance.session.time,
        }
        session_teacher_info.append(session_data)
    # Loop through the sessions taught by the teacher
    for session in sessions_taught:
        # Find all attendance records for the current session
        attendances = Attendance.objects.filter(session=session)

        # Loop through the attendance records
 
        for attendance in attendances:
                            # Check if the attendance record has a student
            if ( attendance.student is not None ) :
            
                    session_data = {
                                    'group': attendance.student.group_number.group_name,
                                    'student_name': f'{attendance.student.user.first_name} {attendance.student.user.last_name}',
                                    'module': session.teacher.module,
                                    'class_name': session.class_name,
                                    'time': session.time,
                                        }
                    session_students_info.append(session_data)
    return render(request, 'AI/teachers/dashboard_teachers.html', {'session_teacher_info': session_teacher_info,'session_students_info': session_students_info,'user_info': user_info})

@login_required(login_url='login')
@forAdmins
def admin_attandance_dashboard(request):
    admin_info = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }

    # Get the teacher's sessions
    attendances = Attendance.objects.all()
  
    # Create a list to store session information for rendering in the template
    session_teachers_info = []
    session_students_info = []
   
    # Loop through the teacher's sessions
    for attendance in attendances:
        if attendance.teacher is not None :
            print('------------------------------------------------------------------',attendance.session.time)
            session_data = {
                'group': attendance.session.group.group_name,
                'teacher_name':f'{attendance.teacher.user.first_name} {attendance.teacher.user.last_name}',
                'class_name': attendance.session.class_name,
                'module': attendance.teacher.module,
                'time': attendance.session.time,
            }
            session_teachers_info.append(session_data)
    # Loop through the sessions taught by the teacher
    for attendance in attendances:
            if attendance.student is not None :
                session_data = {
                    'group': attendance.student.group_number,
                    'student_name': f'{attendance.student.user.first_name} {attendance.student.user.last_name}',
                    'class_teacher':f'{attendance.session.teacher.user.first_name} {attendance.session.teacher.user.last_name}',
                    'module': attendance.session.teacher.module,
                    'class_name': attendance.session.class_name,
                    'time': attendance.session.time,
                }
                session_students_info.append(session_data)
    return render(request, 'AI/administration/attandance_list.html', {'session_teachers_info': session_teachers_info,'session_students_info': session_students_info,'user_info': admin_info})


@login_required(login_url='login')
@forAdmins
def admin_dashboard(request):
    admin_info = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }

    if request.method == 'POST':
        form = SetSessionForm(request.POST)
        form1 = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            form.save()
            print("session created")
        else:
            print("SetSessionForm errors:", form.errors)

        if form1.is_valid():
            # Extract data from form submission
            id_number = request.POST.get('id_number')
            contact_phone = request.POST.get('contact_phone')
            group_name = request.POST.get('group_name')
            Module = request.POST.get('Module')
            position = request.POST.get('position')
            is_supervisor=request.POST.get('is_supervisor')
            if form1.cleaned_data['role'] == "STUDENT":
                user = form1.save()  
                print('User created')
                group_number = GR_number.objects.get(group_name=group_name)
                Student.objects.create(
                    #  created_by=request.user,
                    user=user,
                    id_number=id_number,
                    contact_phone=contact_phone,
                    group_number=group_number
                )
            if request.user.is_superuser and form1.cleaned_data['role'] == "ADMIN":
                    if is_supervisor == 'YES':
                        user = form1.save(is_staff=True,is_superuser=True) 
                    elif  is_supervisor == 'NO':  
                        user = form1.save() 
                    Administration.objects.create(
                            # created_by=request.user,
                            user=user,
                            id_number=id_number,
                            contact_phone=contact_phone,
                        )
            if form1.cleaned_data['role'] == "TEACHER":
                user = form1.save()  
                print('User created')
                Teacher.objects.create(
                    #  created_by=request.user,
                    user=user,
                    id_number=id_number,
                    contact_phone=contact_phone,
                    module=Module.lower(),
                )
            if form1.cleaned_data['role'] == "TECHNICAL_TEAM":
                user = form1.save()  
                print('User created')
                TechnicalTeam.objects.create(
                    #  created_by=request.user,
                    user=user,
                    id_number=id_number,
                    position=position.lower(),
                    contact_phone=contact_phone,
                )     
        else:
            print("UserRegistrationForm errors:", form1.errors)
    else:
        form = SetSessionForm()
        form1 = UserRegistrationForm()
    return render(request, 'AI/administration/dashboard_administration.html', {'form': form, 'form1': form1, 'admin_info': admin_info})

#    -------------------------------------------- techneical team dash board -------
@login_required(login_url='login_student')
def technical_team_dashboard(request):
    if request.user.role != 'TECHNICAL_TEAM':
        return redirect('login_student')
    return render(request,'AI/technical_team/dashboard_technecal_team.html')



# ---------------------- login --------------------

@notLoggedUsers
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.role == 'STUDENT':
            login(request, user)
            # Redirect to the appropriate student view after successful login
            return redirect('student_dashboard')  # Update with your student dashboard URL
        elif user is not None and user.role == 'ADMIN':
            login(request, user)
            # Redirect to the appropriate admin view after successful login
            return redirect('admin_dashboard')  # Update with your admin dashboard URL            
        elif user is not None and user.role == 'TEACHER':
            login(request, user)
            # Redirect to the appropriate teacher view after successful login
            return redirect('teacher_dashboard')  # Update with your teacher dashboard URL
        elif user is not None and user.role == 'TECHNICAL_TEAM':
            login(request, user)
            # Redirect to the appropriate teacher view after successful login
            return redirect('technical_team_dashboard')  # Update with your teacher dashboard URL
    return render(request, 'AI/user_registration/login_student.html')


# -------------------------------------------------- logout
def userLogout(request):  
    logout(request)
    return redirect('login') 



def create_student(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = StudentForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # Create a new Student instance with the form data but don't save it yet
            new_student = form.save(commit=False)

            # You can perform additional processing or validation here if needed

            # Save the new student to the database
            new_student.save()

            # Optionally, you can redirect to a success page or another view
            return redirect('/index1')  # Replace 'success_page' with the actual URL name or path
    else:
        # If it's not a POST request, create a blank form
        form = StudentForm()

    # Render the HTML template with the form
    return render(request, 'AI/student_form.html', {'form': form})

# ------------------------------ controle settings -------------------



@login_required(login_url='login_student')
def control_settings(request):
    try:
        if request.user.role != 'TECHNICAL_TEAM':
            return redirect('login_student') 
        control_settings = ControlSettingsPublish.objects.first()
        try:
         
            resived_settings = ControlSettingsRecive.objects.first()
            control_settings_data ={
                    'Close_windows': resived_settings.smart_window_status,
                        'power_block_1': resived_settings.block1_status,
                        'power_block_2': resived_settings.block2_status,
                        'power_block_3': resived_settings.block3_status,
                        'water_pump': resived_settings.water_pump_status,
                        
            }
        except Exception as e:
             print(f"the error is -----------------------------------{e}")
        if request.method == 'POST':
            form = ControlSettingsFormPublish(request.POST, instance=control_settings)
            if form.is_valid():
                form.save()
                print('--------------------------------- model saved')
        else:
            form = ControlSettingsFormPublish(instance=control_settings)

        return render(request, 'AI/technical_team/control_settings.html', {'form': form, 'control_settings_data': control_settings_data})
        
    except :
         form = ControlSettingsFormPublish()
         control_settings_data ={
                'Close_windows': False,
                    'power_block_1': False,
                    'power_block_2': False,
                    'power_block_3': False,
                    'water_pump':False}
         return render(request, 'AI/technical_team/control_settings.html', {'form': form, 'control_settings_data': control_settings_data})

# -------react--------------------------------

@login_required(login_url='login_student')
def control_settings_react(request):
        if request.user.role != 'TECHNICAL_TEAM':
            return redirect('login_student') 
        
        return render(request, 'AI/technical_team/control_settings_react.html')
  


