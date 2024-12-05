from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from datetime import datetime

# Create your models here.

class Visitor(models.Model):
    name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10)
    check_in = models.DateTimeField(default=timezone.now)
    check_out = models.DateTimeField(null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

def __str__(self):
    return self.name



