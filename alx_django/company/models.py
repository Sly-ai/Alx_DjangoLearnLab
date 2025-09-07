from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)

class Department(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="departments")
    name = models.CharField(max_length=255)

class Employee(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="employees")
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
