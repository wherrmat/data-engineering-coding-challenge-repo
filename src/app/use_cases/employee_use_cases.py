# app/use_cases/employee_use_cases.py
from domain.models.employee import Employee
from domain.ports.employee_repository import EmployeeRepository

# Create
class CreateEmployeeUseCase:
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    def execute(self, id:int, name: str, date_time: str, department_id: int, job_id: int):
        employee = Employee(id=id, name=name, date_time=date_time, department_id=department_id, job_id=job_id)
        self.employee_repository.save(employee)

# Get by ID
class GetEmployeeUseCase:
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    def execute(self, employee_id: int):
        return self.employee_repository.find_by_id(employee_id)

# Delete
class DeleteEmployeeUseCase:
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    def execute(self, employee_id: int):
        self.employee_repository.delete(employee_id)