from django.db import models
from .forms import DateInput
# Create your models here.

class TimelapseModel(models.Model):
    start = models.DateField(DateInput)
    end = models.DateField(DateInput)
