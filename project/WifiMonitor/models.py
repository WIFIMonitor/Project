from django.db import models
# Create your models here.

class Departments(models.Model):
    name = models.CharField(max_length=30)
    people = models.IntegerField()
    
    def __str__(self):
        return self.name
