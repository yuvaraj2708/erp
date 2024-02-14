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
from datetime import timedelta



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

    return render(request, 'add_building.html', {'form': form, 'clients': clients, 'suppliers': suppliers})

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
            return redirect('employee_list')  # Change 'building_list' to your actual building list URL
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

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)  # Save the form data without committing to the database

            project.save()  # Now, save the main project data to the database

            return redirect('project_list')  # Change 'project_list' to your actual project list URL
        else:
            print(form.errors)  # Add this line to debug form errors
    else:
        form = ProjectForm()

    return render(request, 'add_project.html', {'form': form, 'clients': clients, 'buildings': buildings})

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
    Projectlist = Project.objects.all()
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
def add_attendance(request):
    employees = Employee.objects.all()
    
    if request.method == 'POST':
        attendance_date = request.POST.get('date', None)

        if attendance_date:
            for employee in employees:
                present_key = f"present_{employee.id}"
                leave_key = f"leave_{employee.id}"
                reason_key = f"reason_{employee.id}"

                present = request.POST.get(present_key)
                leave = request.POST.get(leave_key)
                reason = request.POST.get(reason_key, "")

                attendance, created = Attendance.objects.get_or_create(
                    employee=employee,
                    date=attendance_date,
                    defaults={'present': False, 'leave': False, 'reason': ""}
                )

                attendance.present = present == 'on'
                attendance.leave = leave == 'on'
                attendance.reason = reason
                attendance.save()

            return redirect('attendance_list')

    context = {'employees': employees}
    return render(request, 'add_attendance.html', context)
    
@login_required    
def attendance_list(request):
    attendancelist= Attendance.objects.all()

    return render(request,'attendance_list.html',{'attendancelist':attendancelist})

@login_required
def edit_attendance(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    today = date.today()

    try:
        attendance = Attendance.objects.get(employee=employee, date=today)
    except Attendance.DoesNotExist:
        return redirect('add_attendance')  # Redirect to add attendance page if record doesn't exist

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

    return render(request, 'edit_attendance.html', {'employee': employee, 'attendance': attendance})

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

@login_required
def salarysheet(request):
    employees = Employee.objects.all()
    salary_data = []

    for employee in employees:
        total_days = Attendance.objects.filter(employee=employee).count()
        present_days = employee.total_working_days()
        salary_data.append({
            'employee': employee,
            'total_days': total_days,
            'present_days': present_days,
        })

    context = {'salary_data': salary_data}
    return render(request, 'salarysheet.html', context)
   


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
def generate_excel(request):
    try:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="supplierprojects.xlsx"'

        wb = Workbook()
        ws = wb.active

        # Add headers
        headers = [
            "Client Name", "Building Name", "Starting Date", "Finishing Date", "No of Days",
            "LPO", "Invoice No", "VAT", "Amount", "Total Amount", "Payable Pending",
            "Comments", "Paid"
        ]
        ws.append(headers)

        # Add data
        supplierprojects = Supplierproject.objects.all()
        for supplier in supplierprojects:
            data_row = [
                supplier.supplier_Name, supplier.Building_Name, supplier.Starting_Date,
                supplier.Finishing_Date, supplier.No_of_Days, supplier.LPO,
                supplier.Invoice_No, supplier.VAT, supplier.Amount, supplier.Total_Amount,
                supplier.payable_Pending, supplier.Comments, supplier.paid
            ]
            ws.append(data_row)

        wb.save(response)
        return response

    except Exception as e:
        # Print the exception for debugging purposes
        print(f"Error generating Excel: {e}")
        # You can customize the error response as needed
        return HttpResponseServerError("Error generating Excel file.")

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