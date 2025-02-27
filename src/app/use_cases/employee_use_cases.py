# app/use_cases/employee_use_cases.py
from flask import Request, jsonify
from domain.models.employee import Employee
from domain.ports.employee_repository import EmployeeRepository
import os, csv


# Create
class CreateEmployeesUseCase:
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    def execute(self, request: Request):
        try:
            data = request.get_json()
            
            if not isinstance(data, list):
                return jsonify({"error": "The body must be a list of employees"}), 400
            
            if len(data) < 1 or len(data) > 1000:
                return jsonify({"error": "You can only insert between 1 and 1000 employees"}), 400
            
            for index, item in enumerate(data):
                if item[0] is None:
                    return jsonify({"error": f"employee at index {index} must have 'id'"}), 400

            for item in data:
                name = item[1] if item[1] else None
                datetime = item[2] if item[2] else None
                department_id = item[3] if item[3] else None
                job_id = item[4] if item[4] else None
                
                self.employee_repository.save(Employee(id=item[0], name=name, datetime=datetime, department_id=department_id, job_id=job_id))
            
            return jsonify({"message": "employees succesfully created"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

class LoadEmployeesFileUseCase:
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    def execute(self, request: Request):
        if 'file' not in request.files:
            return jsonify({"error": "No file attached"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No attached file"}), 400

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
                        name = employee[1] if employee[1] else None
                        datetime = employee[2] if employee[2] else None
                        department_id = employee[3] if employee[3] else None
                        job_id = employee[4] if employee[4] else None
                        
                        self.employee_repository.save(Employee(id=employee[0], name=name, datetime=datetime, department_id=department_id, job_id=job_id))

                os.remove(file_path)
                return jsonify({"message": f"{len(rows)} rows successfully uploaded", "data": rows}), 201
            except Exception as e:
                os.remove(file_path)
                return jsonify({"error": f"Error processing the CSV file: {str(e)}"}), 500
        else:
            return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400

# Get all
class GetEmployeesUseCase:
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    def execute(self):
        try:
            employees = self.employee_repository.get_all()
            if employees:
                employees_list = [{"id": employee.id, "name": employee.name, "datetime": employee.datetime, "department_id": employee.department_id, "job_id": employee.job_id} for employee in employees]
                return jsonify(employees_list), 200
            else:
                return jsonify({"error": "No employees"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Delete
class DeleteEmployeesUseCase:
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    def execute(self, request: Request):
        try:
            data = request.get_json()
            
            if not isinstance(data, list):
                return jsonify({"error": "The body must be a list of employee_id"}), 400
            
            if len(data) < 1 or len(data) > 1000:
                return jsonify({"error": "You can only delet between 1 and 1000 employees"}), 400
            
            for employee_id in data:
                self.employee_repository.delete(employee_id)
            
            return jsonify({"message": "employees succesfully deleted"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500