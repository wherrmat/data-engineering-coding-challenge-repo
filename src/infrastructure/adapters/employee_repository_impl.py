# infrastructure/repositories/employee_repository_impl.py
from domain.ports.employee_repository import EmployeeRepository
from domain.models.employee import Employee
from infrastructure.database.database import Database

class EmployeeRepositoryImpl(EmployeeRepository):
    def __init__(self, database: Database):
        self.database = database

    def save(self, employee: Employee):
        query = "INSERT INTO hired_employees (id, name, datetime, department_id, job_id) VALUES (?, ?, ?, ?, ?)"
        self.database.execute(query, (employee.id, employee.name, employee.date_time, employee.department_id, employee.job_id))

    def find_by_id(self, employee_id: int):
        query = "SELECT id, name, datetime, department_id, job_id FROM hired_employees WHERE id = ?"
        self.database.cursor.execute(query, (employee_id))
        result = self.database.cursor.fetchone()
        if result:
            return Employee(id=result[0], name=result[1], date_time=result[2], department_id=result[3], job_id=result[4])
        return None

    def delete(self, employee_id: int):
        query = "DELETE FROM hired_employees WHERE id = ?"
        self.database.execute(query, (employee_id))