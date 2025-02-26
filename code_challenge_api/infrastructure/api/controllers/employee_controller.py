# infrastructure/api/controllers/employee_controller.py
from flask import Blueprint, request, jsonify
from app.use_cases.employee_use_cases import CreateEmployeeUseCase, GetEmployeeUseCase, DeleteEmployeeUseCase
from infrastructure.repositories.employee_repository_impl import EmployeeRepositoryImpl
from infrastructure.database.database import Database

employee_blueprint = Blueprint('employee', __name__)

database = Database()
employee_repository = EmployeeRepositoryImpl(database)
create_employee_use_case = CreateEmployeeUseCase(employee_repository)
get_employee_use_case = GetEmployeeUseCase(employee_repository)
delete_employee_use_case = DeleteEmployeeUseCase(employee_repository)

# Create
@employee_blueprint.route('/employee', methods=['POST'])
def create_employee():
    data = request.get_json()

    id = data.get('id')
    name = data.get('name')
    date_time = data.get('date_time')
    department_id = data.get('department_id')
    job_id = data.get('job_id')

    if not id or not name or not date_time or not department_id or not job_id:
        return jsonify({"error": "Missed necessary fields"}), 400

    try:
        create_employee_use_case.execute(id, name, date_time, department_id, job_id)
        return jsonify({"message": "Employee succesfully created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get by ID
@employee_blueprint.route('/employee/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    try:
        employee = get_employee_use_case.execute(employee_id)
        if employee:
            return jsonify({
                "id": employee.id,
                "name": employee.name,
                "date_time": employee.date_time,
                "department_id": employee.department_id,
                "job_id": employee.job_id
            }), 200
        else:
            return jsonify({"error": "Employee not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Delete
@employee_blueprint.route('/employee/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    try:
        delete_employee_use_case.execute(employee_id)
        return jsonify({"message": "Employe succesfully deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400