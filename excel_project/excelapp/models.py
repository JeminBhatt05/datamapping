from django.db import models
from django.core.validators import RegexValidator

class Employe(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)
    mn = models.CharField(max_length=15)
    language = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# class User(models.Model):
#     name=models.CharField(max_length=100)
#     mobile_regex=RegexValidator(regex=r'^\+?1?\d{9,12}$', message="Please enter valid mobile number")
#     mobile_number=models.CharField(validators=[mobile_regex], max_length=12, blank=False, unique=True)
#     email=models.EmailField(unique=True)
#     pwd=models.CharField(max_length=100)
#     cpwd=models.CharField(max_length=100)
    
    
    