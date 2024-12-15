from django.db import models
from django.utils import timezone
from users.models import CustomUser



# class Semester (models.Model):
#     Semester = models.CharField(choices=[('Semester1', 'Semester1'), ('Semester2', 'Semester2')])
#     year = models.CharField(choices=[('L1', 'L1'), ('L2', 'L2'),('L3', 'L3'),('M1', 'M1'),('M2', 'M2')])
    

class GR_number(models.Model):
    group_name = models.CharField(max_length=100)

    def __str__(self):
        return self.group_name


class Student(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': CustomUser.Role.STUDENT},
        related_name='student_profiles',
        null=True,
        blank=False
    )
    created_by= models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        limit_choices_to={'role': CustomUser.Role.ADMIN},
        related_name='created_students',
        null=True,
        blank=False
    )
    id_number = models.CharField(max_length=20, default="0123456789")
    contact_phone = models.CharField(max_length=15, default="213-540-028-098")
    group_number = models.ForeignKey(GR_number, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    

class Teacher(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': CustomUser.Role.TEACHER},
        related_name='teacher_profiles',
        null=True,
        blank=False
    )
    id_number = models.CharField(max_length=20, default="0123456789")
    module = models.CharField(max_length=100,default='not_yet')
    contact_phone = models.CharField(max_length=15, default="213-540-028-098")
    created_by= models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        limit_choices_to={'role': CustomUser.Role.ADMIN},
        related_name='created_teachers',
        null=True,
        blank=False
    )
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    

class Administration(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': CustomUser.Role.ADMIN},
        related_name='administration_profiles',
        null=True,
        blank=False
    )
    created_by= models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        limit_choices_to={'role': CustomUser.Role.ADMIN},
        related_name='created_tadmin_team',
        null=True,
        blank=False
    )
    id_number = models.CharField(max_length=20, default="0123456789")
    position = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15, default="213-540-028-098")
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
class TechnicalTeam (models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': CustomUser.Role.TECHNICAL_TEAM},
        related_name='technicalteam_profiles',
        null=True,
        blank=False
    )
    id_number = models.CharField(max_length=20, default="0123456789")
    position = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15, default="213-540-028-098")
    created_by= models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        limit_choices_to={'role': CustomUser.Role.ADMIN},
        related_name='created_technical_team',
        null=True,
        blank=False
    )
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} '


class SetSession(models.Model):
    group = models.ForeignKey(GR_number, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now) 
    # semester = models.ForeignKey(Semester, related_name='sessions', on_delete=models.SET_NULL,null=True)
    class_name = models.CharField(max_length=50, choices=[('class_1', 'class_1'), ('class_2', 'class_2')])
    def __str__(self):
        return f'{self.time}'


class Attendance(models.Model):
    session = models.ForeignKey(SetSession, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f'{self.session}'


