from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee


import csv
from django.shortcuts import render
from datetime import datetime
# Create your views here.

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})


def upload_employee(request):
    if request.method == 'POST' and request.FILES['file']:
        csv_file = request.FILES['file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        csv_reader = csv.DictReader(decoded_file, delimiter=';')
        for row in csv_reader:
            name = row['Name']
            salary = float(row['Salary'])
            start_date = datetime.strptime(row['Start Date'], '%Y-%m-%d').date()
            annual_salary = salary * 12  # Calculating annual salary
            employee = Employee(name=name, salary=salary, annual_salary=annual_salary, start_date=start_date)
            employee.save()
        
        messages.success(request, 'Archivo CSV subido exitosamente')
        return redirect('employee_list')  # Redirigir a la página employee_list

    return render(request, 'upload_employee.html')