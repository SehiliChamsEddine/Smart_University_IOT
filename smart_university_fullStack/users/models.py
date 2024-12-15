from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        STUDENT = "STUDENT", _("Student")
        TEACHER = "TEACHER", _("Teacher")
        TECHNICAL_TEAM = "TECHNICAL_TEAM", _("Technical Team")
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.ADMIN)

    def __str__(self):
        return f"{self.username} - {self.role}"
