# app/use_cases/department_use_cases.py
from domain.department import Department
from app.ports.department_repository import DepartmentRepository

# Create
class CreateDepartmentUseCase:
    def __init__(self, department_repository: DepartmentRepository):
        self.department_repository = department_repository

    def execute(self, id: int, department_name: str):
        department = Department(id=id, department=department_name)
        self.department_repository.save(department)

# Get by ID
class GetDepartmentUseCase:
    def __init__(self, department_repository: DepartmentRepository):
        self.department_repository = department_repository

    def execute(self, department_id: int):
        return self.department_repository.find_by_id(department_id)

# Delete
class DeleteDepartmentUseCase:
    def __init__(self, department_repository: DepartmentRepository):
        self.department_repository = department_repository

    def execute(self, department_id: int):
        self.department_repository.delete(department_id)