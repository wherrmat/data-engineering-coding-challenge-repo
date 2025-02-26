# infrastructure/api/controllers/department_controller.py
from flask import Blueprint, request, jsonify
from app.use_cases.department_use_cases import CreateDepartmentUseCase, GetDepartmentUseCase, DeleteDepartmentUseCase
from infrastructure.repositories.department_repository_impl import DepartmentRepositoryImpl
from infrastructure.database.database import Database

department_blueprint = Blueprint('department', __name__)

database = Database()
department_repository = DepartmentRepositoryImpl(database)
create_department_use_case = CreateDepartmentUseCase(department_repository)
get_department_use_case = GetDepartmentUseCase(department_repository)
delete_department_use_case = DeleteDepartmentUseCase(department_repository)

# Create
@department_blueprint.route('/department', methods=['POST'])
def create_department():
    data = request.get_json()
    id = data.get('id')
    department = data.get('department')

    if not id or not department:
        return jsonify({"error": "Missed necessary fields"}), 400

    try:
        create_department_use_case.execute(id, department)
        return jsonify({"message": "Department succesfully created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get by ID
@department_blueprint.route('/department/<int:department_id>', methods=['GET'])
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
@department_blueprint.route('/department/<int:department_id>', methods=['DELETE'])
def delete_department(department_id):
    try:
        delete_department_use_case.execute(department_id)
        return jsonify({"message": "Departamnt succesfully deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400