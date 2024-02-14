from django.db import models
import os 
from django.db.models import Sum

# Create your models here.
class Client(models.Model):
    clientname = models.CharField(max_length=255)


    def __str__(self):
        return self.clientname


class Supplier(models.Model):
    supplier_name = models.CharField(max_length=255)

    def __str__(self):
        return self.supplier_name

class Building(models.Model):
    building_name = models.CharField(max_length=255)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.building_name

class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    PROJECT_TYPE_CHOICES = [
    ('AMC', 'AMC'),
    ('LPO', 'LPO'),
    ('Workloader', 'Workloader'),
    ]
    projectype = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES)
    
    cradle_number = models.CharField(max_length=50)
    starting_date = models.DateField()
    finishing_date = models.DateField()
    number_of_days = models.IntegerField()
    team = models.CharField(max_length=255)
    materials_used = models.TextField()
    receipt = models.CharField(max_length=50)
    invoice_number = models.CharField(max_length=50)
    vat = models.DecimalField(max_digits=5, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    income = models.DecimalField(max_digits=10, decimal_places=2)
    receivable_pending = models.DecimalField(max_digits=10, decimal_places=2)
    comments = models.TextField()

    # Fields specific to AMC
    amc_start_date = models.DateField(null=True, blank=True)
    amc_end_date = models.DateField(null=True, blank=True)
    yearly_cycle = models.CharField(max_length=50, choices=[('Yearly 1', 'Yearly 1'), ('Yearly 2', 'Yearly 2'), ('Yearly 3', 'Yearly 3'),('Yearly 4', 'Yearly 4')], null=True, blank=True)

    # Fields specific to LPO
    lpo_field = models.CharField(max_length=50, null=True, blank=True)

    # Fields specific to Workloader
    workloader_type = models.CharField(max_length=50, choices=[('Normal 2', 'Normal 2'), ('Normal 3', 'Normal 3'), ('Critical', 'Critical')], null=True, blank=True)   

class Supplierproject(models.Model):    
   Building_Name = models.ForeignKey(Building, on_delete=models.CASCADE)
   supplier_Name = models.ForeignKey(Supplier, on_delete=models.CASCADE)
   Starting_Date = models.CharField(max_length=255)
   Finishing_Date = models.CharField(max_length=255)
   No_of_Days = models.CharField(max_length=255)
   LPO = models.CharField(max_length=255)
   Invoice_No = models.CharField(max_length=255)
   VAT = models.CharField(max_length=255)
   Amount = models.CharField(max_length=255)
   Total_Amount = models.CharField(max_length=255)
   payable_Pending = models.CharField(max_length=255)
   Comments = models.CharField(max_length=255)
   paid = models.CharField(max_length=255)

class Businessdevelopment(models.Model):    
   Building_Name = models.ForeignKey(Building, on_delete=models.CASCADE)
   client_Name = models.ForeignKey(Client, on_delete=models.CASCADE)
   Starting_Date = models.CharField(max_length=255)
   Finishing_Date = models.CharField(max_length=255)
   No_of_Days = models.CharField(max_length=255)
   LPO = models.CharField(max_length=255)
   Invoice_No = models.CharField(max_length=255)
   Amount = models.CharField(max_length=255)
   Total_Amount = models.CharField(max_length=255)
   payable_Pending = models.CharField(max_length=255)
   Comments = models.CharField(max_length=255)
   paid = models.CharField(max_length=255)


class Employee(models.Model):
    name = models.CharField(max_length=255)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    other_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    building_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Leave_Salary = models.CharField(max_length=255)
    Bonus = models.CharField(max_length=255)
    Overtime = models.CharField(max_length=255) 
    Ticket  = models.CharField(max_length=255)
    LOP = models.CharField(max_length=255)
    Damage_Deduct = models.CharField(max_length=255)
    other_Deduct = models.CharField(max_length=255)
    
    def total_working_days(self):
        return Attendance.objects.filter(employee=self, present=True).count()
   
    
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)
    leave = models.BooleanField(default=False)  # Add this line
    reason = models.CharField(max_length=50)
    def formatted_date(self):
        return self.date.strftime("%Y-%m-%d")
    
    