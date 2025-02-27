# infrastructure/api/controllers/department_controller.py
from flask import Blueprint, request, jsonify
from app.use_cases.department_use_cases import CreateDepartmentUseCase, GetDepartmentUseCase, DeleteDepartmentUseCase
from infrastructure.repositories.department_repository_impl import DepartmentRepositoryImpl
from infrastructure.database.database import Database
import os, csv

department_blueprint = Blueprint('department', __name__)

connection_string = os.getenv("DATABASE_STRING_ODBC_CONNECTION_STRING")
database = Database(connection_string)

upload_folder = os.getenv("UPLOADS_PATH")
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

department_repository = DepartmentRepositoryImpl(database)
create_department_use_case = CreateDepartmentUseCase(department_repository)
get_department_use_case = GetDepartmentUseCase(department_repository)
delete_department_use_case = DeleteDepartmentUseCase(department_repository)

# Create departments from a JSON body request
@department_blueprint.route('/departments', methods=['POST'])
def create_departments():

    try:
        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({"error": "The body must be a list of departments"}), 400
        
        if len(data) < 1 or len(data) > 1000:
            return jsonify({"error": "You can only insert between 1 and 1000 departments"}), 400
        
        for index, department in enumerate(data):
            if 'id' not in department or 'department' not in department:
                return jsonify({"error": f"Department at index {index} must have 'id' and 'department' fields"}), 400

        for department in data:
            create_department_use_case.execute(department['id'], department['department'])
        
        return jsonify({"message": "Departments succesfully created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Load departments from a CSV file
@department_blueprint.route('/departments/csvfile', methods=['POST'])
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
                
                for department in rows:
                    if len(department) != 2:
                        return jsonify({"error": "There are departments without all fields"}), 400
                    
                    create_department_use_case.execute(department[0], department[1])

            os.remove(file_path)
            return jsonify({"message": f"{len(rows)} rows successfully uploaded", "data": rows}), 201
        except Exception as e:
            os.remove(file_path)
            return jsonify({"error": f"Error processing the CSV file: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400


# Get by ID
@department_blueprint.route('/departments/<int:department_id>', methods=['GET'])
def get_department(department_id):
    try:
        department = get_department_use_case.execute(department_id)
        if department:
            return jsonify({
                "id": department.id,
                "department": department.department
            }), 200
        else:
            return jsonify({"error": "Department not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Delete
@department_blueprint.route('/departments/<int:department_id>', methods=['DELETE'])
def delete_department(department_id):
    try:
        delete_department_use_case.execute(department_id)
        return jsonify({"message": "Departamnt succesfully deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400