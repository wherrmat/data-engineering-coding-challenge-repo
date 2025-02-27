# infrastructure/repositories/employee_repository_impl.py
from domain.ports.employee_repository import EmployeeRepository
from domain.models.employee import Employee
from infrastructure.database.database import Database
from typing import List

class EmployeeRepositoryImpl(EmployeeRepository):
    def __init__(self, database: Database):
        self.database = database

    def save(self, employee: Employee):
        query = "INSERT INTO hired_employees (id, name, datetime, department_id, job_id) VALUES (?, ?, ?, ?, ?)"
        self.database.execute(query, (employee.id, employee.name, employee.datetime, employee.department_id, employee.job_id))

    def get_all(self) -> List[Employee]:
        query = "SELECT id, name, datetime, department_id, job_id FROM hired_employees"
        result = self.database.fetch_all(query)
        return result if result else None

    def delete(self, employee_id: int):
        query = "DELETE FROM hired_employees WHERE id = ?"
        self.database.execute(query, (employee_id))