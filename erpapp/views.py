# clients/views.py
from django.shortcuts import render, redirect
from .models import *
from django.http import Http404
from .forms import *
from datetime import date
from django.forms import formset_factory
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from openpyxl import Workbook
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import HttpResponseServerError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta,datetime
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with the URL name of your home page
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission. Please try again.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('login') 

@login_required
def home(request):
    project = Project.objects.all()
    return render(request,'home.html',{'project':project})

@receiver(post_save, sender=Project)
def notify_for_yearly_cycle(sender, instance, **kwargs):
    # Check if the project type is 'AMC' and yearly cycle is 'Yearly 1'
    if instance.projectype == 1 and instance.yearly_cycle == 'Yearly 1':
        try:
            # Notify every 5 seconds for a date range
            for day in range((instance.starting_date - instance.finishing_date).days + 1):
                notify_time = instance.starting_date + timedelta(days=day)
                messages.success(instance.request, f"Notification: Check Yearly 1 for {instance.name} on {notify_time}")
        except ObjectDoesNotExist:
            pass



@login_required
def add_building(request):
    clients = Client.objects.all()
    suppliers = Supplier.objects.all()

    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('building_list')  # Change 'building_list' to your actual building list URL
    else:
        form = BuildingForm()

    return render(request, 'add_building.html', {'form': form})

@login_required
def edit_building(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    clients = Client.objects.all()
    suppliers = Supplier.objects.all()

    if request.method == 'POST':
        form = BuildingForm(request.POST, instance=building)
        if form.is_valid():
            form.save()
            return redirect('building_list')  # Change 'building_list' to your actual building list URL
    else:
        form = BuildingForm(instance=building)

    return render(request, 'edit_building.html', {'form': form, 'clients': clients, 'suppliers': suppliers, 'building': building})    

@login_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'edit_employee.html', {'form': form, 'employee': employee})


@login_required
def add_client(request):
    if request.method == 'POST':
        client_name = request.POST['clientname']
        Client.objects.create(clientname=client_name)
        return redirect('client_list')  # Change 'client_list' to your actual client list URL

    return render(request, 'add_client.html')

@login_required
def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        client.clientname = request.POST.get('clientname', '')
        client.save()
        return redirect('client_list')

    return render(request, 'edit_client.html', {'client': client})

@login_required
def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == 'POST':
        supplier.supplier_name = request.POST.get('supplier_name', '')
        supplier.save()
        return redirect('supplier_list')

    return render(request, 'edit_supplier.html', {'supplier': supplier})

@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})

@login_required
def building_list(request):
    buildings = Building.objects.all()
    return render(request, 'building_list.html', {'buildings': buildings})

@login_required
def add_supplier(request):
    if request.method == 'POST':
        supplier_name = request.POST['supplier_name']
        Supplier.objects.create(supplier_name=supplier_name)
        return redirect('supplier_list')  # Change 'supplier_list' to your actual supplier list URL

    return render(request, 'add_supplier.html')

@login_required
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier_list.html', {'suppliers': suppliers})

@login_required
def add_project(request):
    clients = Client.objects.all()
    buildings = Building.objects.all()
    suppliers = Supplier.objects.all()

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)

            # Check if an existing client is selected
            if form.cleaned_data['existing_clients']:
                project.client = form.cleaned_data['existing_clients']
            else:
                # Use the new client name if an existing client is not selected
                new_client_name = form.cleaned_data['new_client']

                # Check if the client with the given name already exists
                existing_client = Client.objects.filter(clientname=new_client_name).first()

                if existing_client:
                    project.client = existing_client
                else:
                    # Create a new client and assign it to the project
                    new_client = Client.objects.create(clientname=new_client_name)
                    project.client = new_client

            # Check if an existing building is selected
            if form.cleaned_data['existing_buildings']:
                project.building = form.cleaned_data['existing_buildings']
            else:
                # Use the new building name if an existing building is not selected
                new_building_name = form.cleaned_data['new_building']

                # Check if the building with the given name already exists
                existing_building = Building.objects.filter(building_name=new_building_name).first()

                if existing_building:
                    project.building = existing_building
                else:
                    # Create a new building and assign it to the project
                    new_building = Building.objects.create(building_name=new_building_name)
                    project.building = new_building

                 # supplier
                if form.cleaned_data['existing_subcontrators']:
                   project.SubcontratorName = form.cleaned_data['existing_subcontrators']
                else:
                # Use the new building name if an existing building is not selected
                    new_supplier_name = form.cleaned_data['new_subcontrator']

                # Check if the building with the given name already exists
                    existing_subcontrators = Supplier.objects.filter(supplier_name=new_supplier_name).first()

                    if existing_subcontrators:
                        project.SubcontratorName = existing_subcontrators
                    else:
                        # Create a new building and assign it to the project
                        new_subcontrator = Supplier.objects.create(supplier_name=new_supplier_name)
                        project.SubcontratorName = new_subcontrator

            project.save()
            return redirect('project_list')
        else:
            print(form.errors)
    else:
        form = ProjectForm()

    return render(request, 'add_project.html', {'form': form, 'clients': clients, 'buildings': buildings, 'suppliers': suppliers})

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('employee_list')  # Change 'building_list' to your actual building list URL
    else:
        form = ProjectForm(instance=project)

    return render(request, 'edit_project.html', {'form': form, 'project': project}) 

@login_required
def edit_supplierproject(request, supplierproject_id):
    supplierproject = get_object_or_404(Supplierproject, pk=supplierproject_id)
    if request.method == 'POST':
        form = SupplierprojectForm(request.POST, instance=supplierproject)
        if form.is_valid():
            form.save()
            return redirect('supplierproject_list') 
    else:
        form = SupplierprojectForm(instance=supplierproject)

    return render(request, 'edit_supplierproject.html', {'form': form, 'supplierproject': supplierproject}) 

@login_required
def edit_businessdevelopment(request, businessdevelopment_id):
    businessdevelopment = get_object_or_404(Businessdevelopment, pk=businessdevelopment_id)
    if request.method == 'POST':
        form = businessdevelopmentForm(request.POST, instance=businessdevelopment)
        if form.is_valid():
            form.save()
            return redirect('businessdevelopment_list') 
    else:
        form = businessdevelopmentForm(instance=businessdevelopment)

    return render(request, 'edit_businessdevelopment.html', {'form': form, 'businessdevelopment': businessdevelopment}) 


@login_required
def businessdevelopment(request):
    if request.method == 'POST':
        form = businessdevelopmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('businessdevelopment_list')
    else:
        form = businessdevelopmentForm()

    return render(request, 'add_businessdevelopment.html', {'form': form})  

@login_required
def businessdevelopment_list(request):
    businessdevelopment = Businessdevelopment.objects.all()
    return render(request, 'businessdevelopment_list.html', {'businessdevelopment': businessdevelopment})


@login_required
def project_list(request):
    from_date_str = request.GET.get('from_date')
    to_date_str = request.GET.get('to_date')

    # Validate and convert date strings to datetime objects
    try:
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d') if from_date_str else None
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d') if to_date_str else None
    except ValueError:
        # Handle invalid date format if needed
        # You might want to redirect to an error page or display an error message
        return render(request, 'error.html', {'error_message': 'Invalid date format'})

    # Use Q objects to construct complex queries
    filter_conditions = Q()
    if from_date:
        filter_conditions &= Q(starting_date__gte=from_date)
    if to_date:
        filter_conditions &= Q(finishing_date__lte=to_date)

    # Apply the filters to the queryset
    Projectlist = Project.objects.filter(filter_conditions)

    return render(request, 'project_list.html', {'Projectlist': Projectlist})

@login_required
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')  # Change 'employee_list' to your actual employee list URL
    else:
        form = EmployeeForm()

    return render(request, 'add_employee.html', {'form': form})

@login_required
def add_salary(request):
    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            salary_instance = form.save(commit=False)
            total = salary_instance.calculate_total()
            salary_instance.total = total  # Add a 'total' field in your model to store the calculated value
            salary_instance.save()
            return redirect('salary_list')
    else:
        form = SalaryForm()

    return render(request, 'add_salary.html', {'form': form})

@login_required
def salary_list(request):
    if request.method == 'GET':
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        employee_name = request.GET.get('employee_name')
        # Assuming your date format is 'YYYY-MM-DD'
        date_format = '%Y-%m-%d'
        
        salary = Salary.objects.all()

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, date_format)
            end_date = datetime.strptime(end_date_str, date_format)
            # Filter salary queryset based on date range
            salary = Salary.objects.filter(date__range=(start_date, end_date))
        
        if employee_name:
            salary = salary.filter(employee_name__employeename=employee_name)

       

    return render(request, 'salary_list.html', {'salary': salary})


@login_required
def edit_salary(request, salary_id):
    salary = get_object_or_404(Salary, pk=salary_id)

    if request.method == 'POST':
        form = SalaryForm(request.POST, instance=salary)
        if form.is_valid():
            form.save()
            return redirect('salary_list')
        
    else:
        form = SalaryForm(instance=salary)

    return render(request, 'edit_salary.html', {'form': form, 'salary': salary})

@login_required
def add_allowance(request):
    if request.method == 'POST':
        form = allowanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allowance_list')  # Change 'employee_list' to your actual employee list URL
    else:
        form = allowanceForm()

    return render(request, 'add_allowance.html', {'form': form})

@login_required
def allowance_list(request):
    if request.method == 'GET':
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        employeename = request.GET.get('employeename')
        
        # Assuming your date format is 'YYYY-MM-DD'
        date_format = '%Y-%m-%d'

        # Initialize queryset without filtering
        allowances = allowance.objects.all()

        # Apply date range filter if start_date and end_date provided
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, date_format)
            end_date = datetime.strptime(end_date_str, date_format)
            allowances = allowances.filter(date__range=(start_date, end_date))

        # Apply employee name filter if employeename provided
        if employeename:
            allowances = allowances.filter(employeename__employeename=employeename)
        
        total_allowance = allowances.aggregate(Sum('allowance'))['allowance__sum']

    return render(request, 'allowance_list.html', {'allowances': allowances, 'total_allowance': total_allowance})

@login_required
def edit_allowance(request, allowance_id):
    editallowance = get_object_or_404(allowance, pk=allowance_id)

    if request.method == 'POST':
        form = allowanceForm(request.POST, instance=editallowance)
        if form.is_valid():
            form.save()
            return redirect('allowance_list')
    else:
        form = allowanceForm(instance=editallowance)

    return render(request, 'edit_allowance.html', {'form': form, 'editallowance': editallowance})

@login_required
def add_attendance(request):
    employees = Employee.objects.all()
    
    if request.method == 'POST':
        attendance_date = request.POST.get('date', None)

        if attendance_date:
            today_date = datetime.today().strftime('%Y-%m-%d')

            for employee in employees:
                present_key = f"present_{employee.id}"
                absent_key = f"absent_{employee.id}"
                reason_key = f"reason_{employee.id}"

                present = request.POST.get(present_key)
                absent = request.POST.get(absent_key)
                reason = request.POST.get(reason_key, "")

                # Get today's attendance record or create a new one
                attendance, created = Attendance.objects.get_or_create(
                    employee=employee,
                    date=today_date,
                    defaults={'present': False, 'absent': False, 'reason': ""}
                )

                attendance.present = present == 'on'
                attendance.absent = absent == 'on'
                attendance.reason = reason
                attendance.save()

            return redirect('attendance_list')

    context = {'employees': employees}
    return render(request, 'add_attendance.html', context)
    
@login_required    
def attendance_list(request):
    if request.method == 'GET':
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        employee = request.GET.get('employee')
        # Assuming your date format is 'YYYY-MM-DD'
        date_format = '%Y-%m-%d'
        attendancelist = Attendance.objects.all()

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, date_format)
            end_date = datetime.strptime(end_date_str, date_format)
            # Filter salary queryset based on date range
            attendancelist = Attendance.objects.filter(date__range=(start_date, end_date))
        
        if employee:
            attendancelist = attendancelist.filter(employee__employeename=employee)
        


    return render(request,'attendance_list.html',{'attendancelist':attendancelist})


@login_required
def edit_attendance(request, atttendance_id):
    attendance = get_object_or_404(Attendance, id=atttendance_id)
    today = date.today()


    if request.method == 'POST':
        present = request.POST.get('present') == 'on'
        absent = request.POST.get('absent') == 'on'
        reason = request.POST.get('reason', '')

        # Update the existing attendance record
        attendance.present = present
        attendance.absent = absent
        attendance.reason = reason
        attendance.save()

        return redirect('attendance_list')  # Redirect to a success page or another page after editing

    return render(request, 'edit_attendance.html', {'attendance': attendance})

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})


   


@login_required
def supplierproject_list(request):
    supplierprojects = Supplierproject.objects.all()
    return render(request, 'supplierproject_list.html', {'supplierprojects': supplierprojects})

@login_required
def add_supplierproject(request):
    if request.method == 'POST':
        form = SupplierprojectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplierproject_list')
    else:
        form = SupplierprojectForm()

    return render(request, 'add_supplierproject.html', {'form': form})



@login_required
def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="supplierprojects.pdf"'

    # Create PDF document
    p = canvas.Canvas(response)
    width, height = letter
    p.setPageSize((width, height))

    # Add data to PDF
    supplierprojects = Supplierproject.objects.all()
    data = []
    for supplier in supplierprojects:
        data.append([
            supplier.supplier_Name, supplier.Building_Name, supplier.Starting_Date,
            supplier.Finishing_Date, supplier.No_of_Days, supplier.LPO,
            supplier.Invoice_No, supplier.VAT, supplier.Amount, supplier.Total_Amount,
            supplier.payable_Pending, supplier.Comments, supplier.paid
        ])

    # Define table styles
    table_style = [
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ]

    # Create PDF table
    table = Table(data, style=table_style)
    table.wrapOn(p, width, height)
    table.drawOn(p, 30, height - 200)

    p.showPage()
    p.save()

    return response



def account_multi_form(request):
   extra_forms = 2  # Set the initial number of extra forms

   if request.method == 'POST':
        formset = TallyEntryFormSet(request.POST, form_kwargs={'empty_permitted': True})
        if formset.is_valid():
            entry_collection, created = TallyEntryCollection.objects.get_or_create(
                collection_date=date.today()
            )
            for form in formset:
                if form.has_changed():  # Only save forms with changes
                    account_entry = form.save(commit=False)
                    account_entry.entry_collection = entry_collection
                    account_entry.save()
            return redirect('account_list')
   else:
        formset = TallyEntryFormSet(queryset=Account.objects.none(), form_kwargs={'empty_permitted': True})

    # Add extra forms to the formset
   for _ in range(extra_forms):
        formset.forms.append(formset.empty_form)

   return render(request, 'account_multi_form.html', {'formset': formset})

def account_list(request):
    if request.method == 'GET':
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        date_format = '%Y-%m-%d'

        accounts = Account.objects.all()

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, date_format)
            end_date = datetime.strptime(end_date_str, date_format)
       

    # Filter accounts based on date range
            accounts = Account.objects.filter(entry_collection__collection_date__range=[start_date, end_date])

    total_debit = accounts.aggregate(Sum('deb'))['deb__sum']
    total_credit = accounts.aggregate(Sum('credit'))['credit__sum']
    total = total_debit - total_credit
    return render(request, 'account_list.html', {'accounts': accounts, 'total_debit': total_debit, 'total_credit': total_credit,'total':total})

@login_required
def edit_account(request, entry_id):
    entry = get_object_or_404(Account, id=entry_id)
    entry_collection = entry.entry_collection

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('account_list')  # Redirect to the success page or any other page as needed
    else:
        form = AccountForm(instance=entry)

    return render(request, 'edit_account.html', {'form': form, 'entry_collection': entry_collection}) 