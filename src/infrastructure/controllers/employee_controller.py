# infrastructure/api/controllers/employee_controller.py
from flask import Blueprint, request, jsonify
from app.use_cases.employee_use_cases import CreateEmployeeUseCase, GetEmployeeUseCase, DeleteEmployeeUseCase
from infrastructure.adapters.employee_repository_impl import EmployeeRepositoryImpl
from infrastructure.database.database import Database
import os, csv

employee_blueprint = Blueprint('employee', __name__)

connection_string = os.getenv("DATABASE_STRING_ODBC_CONNECTION_STRING")
database = Database(connection_string)

upload_folder = os.getenv("UPLOADS_PATH")
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)
    
employee_repository = EmployeeRepositoryImpl(database)
create_employee_use_case = CreateEmployeeUseCase(employee_repository)
get_employee_use_case = GetEmployeeUseCase(employee_repository)
delete_employee_use_case = DeleteEmployeeUseCase(employee_repository)

# Create empployees from a JSON body request
@employee_blueprint.route('/employees', methods=['POST'])
def create_employees():
    
    try:
        data = request.get_json()

        if not isinstance(data, list):
            return jsonify({"error": "The body must be a list of employees"}), 400
        
        if len(data) < 1 or len(data) > 1000:
            return jsonify({"error": "You can only insert between 1 and 1000 employees"}), 400
        
        for index, employee in enumerate(data):
            if 'id' not in employee:
                return jsonify({"error": f"employee at index {index} must have 'id'"}), 400
        
        for employee in data:
            name = employee.get('name', None)
            datetime = employee.get('datetime', None)
            department_id = employee.get('department_id', None)
            job_id = employee.get('job_id', None)

            create_employee_use_case.execute(employee['id'], name, datetime, department_id, job_id)

        return jsonify({"message": "Employees succesfully created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Load employees from a CSV file
@employee_blueprint.route('/employees/csvfile', methods=['POST'])
def upload_csv():
    
    if 'file' not in request.files:
        return jsonify({"error": "No file attached"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.csv'):
        
        file_path = os.path.join(os.getenv("UPLOADS_PATH"), file.filename)
        file.save(file_path)

        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                rows = [row for row in csvreader]
                csvfile.close()

                if len(rows) < 1 or len(rows) > 1000:
                    os.remove(file_path)
                    return jsonify({"error": "You can only attach files with 1 - 1000 records"}), 400

                for employee in rows:
                    if not employee[0]:
                        return jsonify({"error": "There are employees without id"}), 400
                    
                    name = employee[1] if employee[1] else None
                    datetime = employee[2] if employee[2] else None
                    department_id = employee[3] if employee[3] else None
                    job_id = employee[4] if employee[4] else None

                    create_employee_use_case.execute(employee[0], name, datetime, department_id, job_id)

            os.remove(file_path)
            return jsonify({"message": f"{len(rows)} rows successfully uploaded", "data": rows}), 201
        except Exception as e:
            os.remove(file_path)
            return jsonify({"error": f"Error processing the CSV file: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400


# Get by ID
@employee_blueprint.route('/employees/<int:employee_id>', methods=['GET'])
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
@employee_blueprint.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    try:
        delete_employee_use_case.execute(employee_id)
        return jsonify({"message": "Employe succesfully deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400