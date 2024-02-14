# clients/urls.py
from django.urls import path
from .views import * 
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('', home, name='home'),
    path('add_building/', add_building, name='add_building'),
    path('building_list/', building_list, name='building_list'), 
    path('add_client/', add_client, name='add_client'),
    path('client_list/', client_list, name='client_list'),
    path('add_supplier/', add_supplier, name='add_supplier'), 
    path('edit_supplier/<int:supplier_id>/', edit_supplier, name='edit_supplier'),
    path('supplier_list/', supplier_list, name='supplier_list'),
    path('add_project/',add_project,name="add_project"),
    path('edit_project/<int:project_id>/', edit_project, name='edit_project'),
    path('add_employee/',add_employee,name="add_employee"),
    path('add_attendance/',add_attendance,name="add_attendance"),
    path('attendance_list/',attendance_list,name='attendance_list'),
    path('edit_attendance/<int:employee_id>/', edit_attendance, name='edit_attendance'),
    path('employee_list/', employee_list, name='employee_list'),
    path('edit_employee/<int:employee_id>/', edit_employee, name='edit_employee'),
    path('edit_client/<int:client_id>/', edit_client, name='edit_client'),
    path('salarysheet',salarysheet,name='salarysheet'),
    path('project_list/',project_list,name='project_list',),
    path('supplierproject/', supplierproject_list, name='supplierproject_list'),
    path('supplierproject/add/', add_supplierproject, name='add_supplierproject'),
    path('edit_supplierproject/<int:supplierproject_id>/', edit_supplierproject, name='edit_supplierproject'),
    path('generate_excelsupplierproject/', generate_excel, name='generate_excel'),
    path('generate_pdfsupplierproject/', generate_pdf, name='generate_pdf'),
    path('edit_building/<int:building_id>/', edit_building, name='edit_building'),
    path('businessdevelopment/', businessdevelopment, name='businessdevelopment'),
    path('businessdevelopment_list/',businessdevelopment_list,name='businessdevelopment_list'),
    path('edit_businessdevelopment/<int:businessdevelopment_id>/', edit_businessdevelopment, name='edit_businessdevelopment'),
  
    # Add other URL patterns as needed
]
