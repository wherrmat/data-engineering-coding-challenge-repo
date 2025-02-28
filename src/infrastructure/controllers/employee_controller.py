# infrastructure/api/controllers/employee_controller.py
from flask import Blueprint, request, jsonify
from app.use_cases.employee_use_cases import CreateEmployeesUseCase, LoadEmployeesFileUseCase, GetEmployeesUseCase, DeleteEmployeesUseCase
from infrastructure.adapters.employee_repository_impl import EmployeeRepositoryImpl
from infrastructure.database.database import Database
import os

upload_folder = os.getenv("UPLOADS_PATH")
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

employee_blueprint = Blueprint('employee', __name__)

connection_string = os.getenv("DATABASE_ODBC_CONNECTION_STRING")
print(connection_string)

employee_repository = EmployeeRepositoryImpl(database)

create_employees_use_case = CreateEmployeesUseCase(employee_repository)
load_employees_file_use_case = LoadEmployeesFileUseCase(employee_repository)
get_employees_use_case = GetEmployeesUseCase(employee_repository)
delete_employees_use_case = DeleteEmployeesUseCase(employee_repository)

# Create employees from a JSON body request
@employee_blueprint.route('/employees', methods=['POST'])
def create_employees():
    return create_employees_use_case.execute(request=request)

# Load employees from a CSV file
@employee_blueprint.route('/employees/csvfile', methods=['POST'])
def upload_departmetns_file():
    return load_employees_file_use_case.execute(request=request)

# Get all employees
@employee_blueprint.route('/employees', methods=['GET'])
def get_employeeS():
    return get_employees_use_case.execute()

# Delete
@employee_blueprint.route('/employees', methods=['DELETE'])
def delete_employees():
    return delete_employees_use_case.execute(request=request)