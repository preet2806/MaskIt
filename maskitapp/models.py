from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.
class company_table(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(null=True,unique=True)
    message = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class employee_table(models.Model):
    company = models.ForeignKey(User,on_delete=models.CASCADE)
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    number = models.IntegerField()
    image1 = models.ImageField(upload_to='maskitapp/images',null=True)
    image2 = models.ImageField(upload_to='maskitapp/images',null=True)
    image3 = models.ImageField(upload_to='maskitapp/images',null=True)
    image4 = models.ImageField(upload_to='maskitapp/images',null=True)
    image5 = models.ImageField(upload_to='maskitapp/images',null=True)
    def __str__(self):
        return self.name
class history_table(models.Model):
    company = models.ForeignKey(User,on_delete=models.CASCADE)
    employee = models.ForeignKey('employee_table',on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now)