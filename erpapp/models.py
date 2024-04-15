from django.db import models
import os 
from django.db.models import Sum
from django.utils import timezone

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
    client = models.CharField(max_length=50)
    building = models.CharField(max_length=50)
    PROJECT_TYPE_CHOICES = [
    ('AMC', 'AMC'),
    ('LPO', 'LPO'),
    ('Workorder', 'Workorder'),
    ]
    projectype = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES)
    cradle_number = models.CharField(max_length=50)
    starting_date = models.DateField(null=True, blank=True)
    finishing_date = models.DateField(null=True, blank=True)
    number_of_days = models.IntegerField()
    team = models.CharField(max_length=255)
    SubcontratorName = models.CharField(max_length=255)
    Buildingtype = models.CharField(max_length=255)
    No_of_Floors = models.CharField(null=True,max_length=255)
    materials_used = models.TextField()
    receipt = models.CharField(max_length=50)
    invoice_number = models.CharField(max_length=50)
    vat = models.DecimalField(max_digits=5, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_received = models.CharField(max_length=255)
    received_date = models.CharField(max_length=255)
    bank_name= models.CharField(max_length=255)
    comments = models.TextField()
    Payable_Pending = models.CharField(max_length=255)
    Subcontrator_invoice = models.CharField(max_length=255)
    cradle_number_input = models.CharField(max_length=255)
    paid = models.CharField(max_length=255)
    paid_date = models.CharField(max_length=255)


    # Fields specific to AMC
    amc_start_date = models.DateField(null=True, blank=True)
    amc_end_date = models.DateField(null=True, blank=True)
    yearly_cycle = models.CharField(max_length=50, choices=[('Yearly 1', 'Yearly 1'), ('Yearly 2', 'Yearly 2'), ('Yearly 3', 'Yearly 3'),('Yearly 4', 'Yearly 4')], null=True, blank=True)

    # Fields specific to LPO
    lpo_field = models.CharField(max_length=50, null=True, blank=True)

    # Fields specific to Workloader
    workorder_type = models.CharField(max_length=50, choices=[('Normal 2', 'Normal 2'), ('Normal 3', 'Normal 3'), ('Critical', 'Critical')], null=True, blank=True)   
    def is_fully_entered(self):
        # Check if all required fields are filled
        required_fields = [self.starting_date, self.finishing_date, self.payment_received]
        return all(field for field in required_fields)
    

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
    employeename = models.CharField(max_length=255)
    date_of_joining = models.CharField(max_length=225)
    passport_number = models.CharField(max_length=255)
    passport_expirydate =  models.CharField(max_length=255)
    eid =  models.CharField(max_length=255)
    eid_expirydate =  models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    operatorcard_expirydate = models.CharField(max_length=255)
    date_of_releiving = models.CharField(max_length=255)

    passportattachment = models.FileField(upload_to='employee_attachments/', null=True, blank=True)
    emiratesattachment = models.FileField(upload_to='employee_attachments/', null=True, blank=True)
    operatorcardattachment = models.FileField(upload_to='employee_attachments/', null=True, blank=True)
    def __str__(self):
        return self.employeename
   
    
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)
    absent = models.BooleanField(default=False)  # Add this line
    reason = models.CharField(max_length=50)
    attachment = models.FileField(upload_to='attendance_attachments/', null=True, blank=True)
    def formatted_date(self):
        return self.date.strftime("%Y-%m-%d")


class TallyEntryCollection(models.Model):
    collection_date = models.DateField(auto_now_add=True)


class Account(models.Model):
    entry_collection = models.ForeignKey(TallyEntryCollection, on_delete=models.CASCADE, related_name='tallyentry_set')
    name = models.CharField(max_length=255)
    bill = models.CharField(max_length=255)
    class_type = models.CharField(max_length=255)
    deb = models.DecimalField(max_digits=10, decimal_places=2)
    credit = models.DecimalField(max_digits=10, decimal_places=2)
    memo = models.CharField(max_length=255)
  

    def save(self, *args, **kwargs):
        self.deb = self.deb if self.deb else 0
        self.credit = self.credit if self.credit else 0
        super().save(*args, **kwargs)


class Salary(models.Model):
    employee_name = models.ForeignKey(Employee ,on_delete=models.CASCADE)
    basic_salary = models.CharField(max_length=255)
    date=models.DateField()
    other_allowance = models.CharField(max_length=255)
    building_allowance = models.CharField(max_length=255)
    leave_salary = models.CharField(max_length=255)
    bonus = models.CharField(max_length=255)
    overtime = models.CharField(max_length=255)
    ticket = models.CharField(max_length=255)
    lop = models.CharField(max_length=255)
    damage_deduct = models.CharField(max_length=255)
    other_deduct = models.CharField(max_length=255)
    
    def calculate_total(self):
        # Convert fields to numeric types before performing calculations
        basic_salary = float(self.basic_salary) if self.basic_salary else 0
        other_allowance = float(self.other_allowance) if self.other_allowance else 0
        building_allowance = float(self.building_allowance) if self.building_allowance else 0
        leave_salary = float(self.leave_salary) if self.leave_salary else 0
        bonus = float(self.bonus) if self.bonus else 0
        overtime = float(self.overtime) if self.overtime else 0
        ticket = float(self.ticket) if self.ticket else 0
        lop = float(self.lop) if self.lop else 0
        damage_deduct = float(self.damage_deduct) if self.damage_deduct else 0
        other_deduct = float(self.other_deduct) if self.other_deduct else 0

        # Perform calculations
        total = (
            basic_salary +
            other_allowance +
            building_allowance +
            leave_salary +
            bonus +
            overtime +
            ticket -
            lop -
            damage_deduct -
            other_deduct
        )
        return total

class allowance(models.Model):
    date=models.DateField()
    employeename = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    building = models.ManyToManyField(Building)
    no_of_days = models.CharField(max_length=255)
    allowance = models.CharField(max_length=255)
    remark = models.CharField(max_length=255)

  
    