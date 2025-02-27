# app/use_cases/department_use_cases.py
from flask import Request, jsonify
from domain.models.department import Department
from domain.ports.department_repository import DepartmentRepository
import os, csv

# Create
class CreateDepartmentsUseCase:
    def __init__(self, department_repository: DepartmentRepository):
        self.department_repository = department_repository

    def execute(self, request: Request):
        try:
            data = request.get_json()
            
            if not isinstance(data, list):
                return jsonify({"error": "The body must be a list of departments"}), 400
            
            if len(data) < 1 or len(data) > 1000:
                return jsonify({"error": "You can only insert between 1 and 1000 departments"}), 400
            
            for index, item  in enumerate(data):
                if item[0] is None or item[1] is None:
                    return jsonify({"error": f"Department at index {index} must have 'id' and 'department' fields"}), 400

            for item in data:
                self.department_repository.save(Department(id=item[0], department=item[1]))
            
            return jsonify({"message": "Departments succesfully created"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

class LoadDepartmentsFileUseCase:
    def __init__(self, department_repository: DepartmentRepository):
        self.department_repository = department_repository

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
                    
                    for department in rows:
                        if len(department) != 2:
                            return jsonify({"error": "There are departments without all fields"}), 400
                        
                        self.department_repository.save(Department(id=department[0], department=department[1]))

                os.remove(file_path)
                return jsonify({"message": f"{len(rows)} rows successfully uploaded", "data": rows}), 201
            except Exception as e:
                os.remove(file_path)
                return jsonify({"error": f"Error processing the CSV file: {str(e)}"}), 500
        else:
            return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400

# Get all
class GetDepartmentsUseCase:
    def __init__(self, department_repository: DepartmentRepository):
        self.department_repository = department_repository

    def execute(self):
        try:
            departments = self.department_repository.get_all()
            if departments:
                departments_list = [{"id": department.id, "department": department.department} for department in departments]
                return jsonify(departments_list), 200
            else:
                return jsonify({"error": "No departments"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Delete
class DeleteDepartmentsUseCase:
    def __init__(self, department_repository: DepartmentRepository):
        self.department_repository = department_repository

    def execute(self, request: Request):
        try:
            data = request.get_json()
            
            if not isinstance(data, list):
                return jsonify({"error": "The body must be a list of department_id"}), 400
            
            if len(data) < 1 or len(data) > 1000:
                return jsonify({"error": "You can only delet between 1 and 1000 departments"}), 400
            
            for department_id in data:
                self.department_repository.delete(department_id)
            
            return jsonify({"message": "Departments succesfully deleted"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500