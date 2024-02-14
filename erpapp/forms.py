# clients/forms.py
from django import forms
from .models import *

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['building_name', 'client', 'supplier']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].widget.attrs.update({'class': 'form-control'})
        self.fields['supplier'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['building_name'].widget.attrs.update({'class': 'form-control'})       

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['building'].widget.attrs.update({'class': 'form-control'})
        

       
 
class SupplierprojectForm(forms.ModelForm):
    class Meta:
        model = Supplierproject
        fields = '__all__'
    def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           self.fields['Building_Name'].widget.attrs.update({'class': 'form-control'})
           self.fields['supplier_Name'].widget.attrs.update({'class': 'form-control'})

class businessdevelopmentForm(forms.ModelForm):
        class Meta:
            model = Businessdevelopment
            fields = '__all__'
        def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           self.fields['client_Name'].widget.attrs.update({'class': 'form-control'})
           self.fields['Building_Name'].widget.attrs.update({'class': 'form-control'})    

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'building', 'basic_salary', 'other_allowance', 'building_allowance', 'Leave_Salary', 'Bonus', 'Overtime', 'Ticket', 'LOP', 'Damage_Deduct', 'other_Deduct']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['building'].widget.attrs.update({'class': 'form-control'})
        self.fields['basic_salary'].widget.attrs.update({'class': 'form-control'})
        self.fields['other_allowance'].widget.attrs.update({'class': 'form-control'})
        self.fields['building_allowance'].widget.attrs.update({'class': 'form-control'})
        self.fields['Leave_Salary'].widget.attrs.update({'class': 'form-control'})
        self.fields['Bonus'].widget.attrs.update({'class': 'form-control'})
        self.fields['Overtime'].widget.attrs.update({'class': 'form-control'})
        self.fields['Ticket'].widget.attrs.update({'class': 'form-control'})
        self.fields['LOP'].widget.attrs.update({'class': 'form-control'})
        self.fields['Damage_Deduct'].widget.attrs.update({'class': 'form-control'})
        self.fields['other_Deduct'].widget.attrs.update({'class': 'form-control'})
        
    

    