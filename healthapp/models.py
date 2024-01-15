from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class product(models.Model):
    name=models.CharField(max_length=100,verbose_name="product name")
    price=models.FloatField()
    pdetails=models.CharField(max_length=500,verbose_name="Product Details")
    CAT=((1,'Medicine'),(2,'Personalcare'),(3,'Unicare'),(4,'Covid19'))   # we are using Tuple 
    cat=models.IntegerField(verbose_name="Category",choices=CAT)
    is_active=models.BooleanField(default=True,verbose_name="Available")
    pimage=models.ImageField(upload_to='image')


class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)


class order(models.Model):
    order_id=models.CharField(max_length=30)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)


class Appointments(models.Model):
    aid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    
    DEPARTMENT_CHOICES = [
        ('dept1', 'Cardiology'),
        ('dept2', 'Neurology'),
        ('dept3', 'Hepatology'),
        ('dept4', 'General Physician'),
    ]
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)

    DOCTOR_CHOICES = [
        ('doctor1', 'Jhon Jackson'),
        ('doctor2', 'Amy Jacob'),
        ('doctor3', 'Jing Who'),
        ('doctor4', 'Jane Anderson'),
        ('doctor5', 'Ricky Nathan'),
        ('doctor6', 'Nelson John'),
        ('doctor7', 'Patrick Shiong'),
        ('doctor8', 'Solange Falade'),
    ]
    doctor = models.CharField(max_length=20, choices=DOCTOR_CHOICES)

    message = models.TextField(default=" ")

class Department(models.Model):
    DEPARTMENT_CHOICES = [
        ('dept1', 'Cardiology'),
        ('dept2', 'Neurology'),
        ('dept3', 'Hepatology'),
        ('dept4', 'General Physician'),
    ]
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)

    DOCTOR_CHOICES = [
        ('doctor1', 'Jhon Jackson'),
        ('doctor2', 'Amy Jacob'),
        ('doctor3', 'Jing Who'),
        ('doctor4', 'Jane Anderson'),
        ('doctor5', 'Ricky Nathan'),
        ('doctor6', 'Nelson John'),
        ('doctor7', 'Patrick Shiong'),
        ('doctor8', 'Solange Falade'),
    ]
    doctor = models.CharField(default='doctor8', max_length=20, choices=DOCTOR_CHOICES)
    is_active=models.BooleanField(default=True,verbose_name="Available")

class Feedback(models.Model):
    uname=models.CharField(max_length=50)
    uemail=models.CharField(max_length=50)
    ucmts=models.CharField(max_length=200)
    EXPERIENCE_CHOICES = [
        ('bad', 'bad '),
        ('good','good' ),
        ('excellent','excellent')
    ]
    rating = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)


class customer_details(models.Model): 
    uname=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    firstname=models.CharField(max_length=50,null=True)
    lastname=models.CharField(max_length=50,null=True)
    mobile=models.BigIntegerField(null=True)
    address=models.CharField(max_length=350,null=True)
    is_active=models.BooleanField(default=True, verbose_name ="Active")
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")

class Appoint_History(models.Model):
    aid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    
    DEPARTMENT_CHOICES = [
        ('dept1', 'Cardiology'),
        ('dept2', 'Neurology'),
        ('dept3', 'Hepatology'),
        ('dept4', 'General Physician'),
    ]
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)

    DOCTOR_CHOICES = [
        ('doctor1', 'Jhon Jackson'),
        ('doctor2', 'Amy Jacob'),
        ('doctor3', 'Jing Who'),
        ('doctor4', 'Jane Anderson'),
        ('doctor5', 'Ricky Nathan'),
        ('doctor6', 'Nelson John'),
        ('doctor7', 'Patrick Shiong'),
        ('doctor8', 'Solange Falade'),
    ]
    doctor = models.CharField(max_length=20, choices=DOCTOR_CHOICES)

    message = models.TextField(default=" ")

