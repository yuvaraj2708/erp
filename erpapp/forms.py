# clients/forms.py
from django import forms
from .models import *
from django.forms import formset_factory
from django.forms import inlineformset_factory

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
    existing_clients = forms.ModelChoiceField(queryset=Client.objects.all(), required=False, empty_label="Select existing client")
    new_client = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Client'}))
    new_building = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Building'}))
    existing_buildings = forms.ModelChoiceField(queryset=Building.objects.all(), required=False, empty_label="Select existing Building")
    new_subcontrator = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter new_subcontrator'}))
    existing_subcontrators = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=False, empty_label="Select existing new_subcontrator")

    class Meta:
        model = Project
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False
        self.fields['client'].widget.attrs.update({'class': 'form-control'})
        self.fields['building'].widget.attrs.update({'class': 'form-control'})
        self.fields['existing_subcontrators'].widget.attrs.update({'class': 'form-control'})
        self.fields['existing_buildings'].widget.attrs.update({'class': 'form-control'})
        self.fields['existing_clients'].widget.attrs.update({'class': 'form-control'})

       
 
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
        fields = ['employeename', 'date_of_joining', 'passport_number', 'passport_expirydate', 'emirate_expirydate', 'operatorcard_expirydate', 'date_of_releiving','attachment']
   
class allowanceForm(forms.ModelForm):
    class Meta:
        model = allowance
        fields =['date','employeename','building','no_of_days','allowance','remark']

    def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           for field_name, field in self.fields.items():
              field.required = False
           self.fields['date'].widget.attrs.update({'class': 'form-control'})
           self.fields['employeename'].widget.attrs.update({'class': 'form-control'})
           self.fields['building'].widget.attrs.update({'class': 'form-control'})
           self.fields['no_of_days'].widget.attrs.update({'class': 'form-control'})
           self.fields['allowance'].widget.attrs.update({'class': 'form-control'})
           self.fields['remark'].widget.attrs.update({'class': 'form-control'})
           


class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields ='__all__'
    def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           for field_name, field in self.fields.items():
              field.required = False
           self.fields['employee_name'].widget.attrs.update({'class': 'form-control'})
           self.fields['basic_salary'].widget.attrs.update({'class': 'form-control'})
           self.fields['date'].widget.attrs.update({'class': 'form-control'})
           self.fields['other_allowance'].widget.attrs.update({'class': 'form-control'})
           self.fields['building_allowance'].widget.attrs.update({'class': 'form-control'})
           self.fields['leave_salary'].widget.attrs.update({'class': 'form-control'})
           self.fields['bonus'].widget.attrs.update({'class': 'form-control'})
           self.fields['overtime'].widget.attrs.update({'class': 'form-control'})
           self.fields['ticket'].widget.attrs.update({'class': 'form-control'})
           self.fields['lop'].widget.attrs.update({'class': 'form-control'})
           self.fields['damage_deduct'].widget.attrs.update({'class': 'form-control'})
           self.fields['other_deduct'].widget.attrs.update({'class': 'form-control'})
           

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ['entry_collection', 'date']
        fields = ['name', 'bill', 'class_type', 'deb', 'credit', 'memo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False
            field.widget.attrs.update({'class': 'form-control'})

        # Modify fields to use ModelChoiceField with a custom widget
     

TallyEntryFormSet = inlineformset_factory(TallyEntryCollection, Account, form=AccountForm, extra=10)

