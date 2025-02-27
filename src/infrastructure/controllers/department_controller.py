# infrastructure/api/controllers/department_controller.py
from flask import Blueprint, request 
from app.use_cases.department_use_cases import CreateDepartmentsUseCase, LoadDepartmentsFileUseCase, GetDepartmentsUseCase, DeleteDepartmentsUseCase
from infrastructure.adapters.department_repository_impl import DepartmentRepositoryImpl
from infrastructure.database.database import Database
import os

upload_folder = os.getenv("UPLOADS_PATH")
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

department_blueprint = Blueprint('department', __name__)

connection_string = os.getenv("DATABASE_STRING_ODBC_CONNECTION_STRING")
database = Database(connection_string)

department_repository = DepartmentRepositoryImpl(database)

create_department_use_case = CreateDepartmentsUseCase(department_repository)
load_departments_file_use_case = LoadDepartmentsFileUseCase(department_repository)
get_departments_use_case = GetDepartmentsUseCase(department_repository)
delete_departments_use_case = DeleteDepartmentsUseCase(department_repository)

# Create departments from a JSON body request
@department_blueprint.route('/departments', methods=['POST'])
def create_departments():
    return create_department_use_case.execute(request=request)

# Load departments from a CSV file
@department_blueprint.route('/departments/csvfile', methods=['POST'])
def upload_departmetns_file():
    return load_departments_file_use_case.execute(request=request)

# Get all departments
@department_blueprint.route('/departments', methods=['GET'])
def get_departmentS():
    return get_departments_use_case.execute()

# Delete
@department_blueprint.route('/departments', methods=['DELETE'])
def delete_departments():
    return delete_departments_use_case.execute(request=request)