from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class company_table(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    message = models.CharField(max_length=100)
class employee_table(models.Model):
    company = models.ForeignKey(User,on_delete=models.CASCADE)
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    number = models.IntegerField()
class picture_table(models.Model):
    employee = models.ForeignKey('employee_table',on_delete=models.CASCADE)
    pictur_id = models.AutoField(primary_key=True)
    picture = models.URLField(max_length=50)
class history_table(models.Model):
    company = models.ForeignKey(User,on_delete=models.CASCADE)
    employee = models.ForeignKey('employee_table',on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)