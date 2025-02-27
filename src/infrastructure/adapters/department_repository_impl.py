# infrastructure/repositories/department_repository_impl.py
from domain.ports.department_repository import DepartmentRepository
from domain.models.department import Department
from infrastructure.database.database import Database
from typing import List

class DepartmentRepositoryImpl(DepartmentRepository):
    def __init__(self, database: Database):
        self.database = database

    def save(self, department: Department):
        query = "INSERT INTO departments (id, department) VALUES (?, ?)"
        self.database.execute(query, (department.id, department.department))

    def get_all(self) -> List[Department]:
        query = "SELECT id, department FROM departments"
        result = self.database.fetch_all(query)
        return result if result else None

    def delete(self, department_id: int):
        query = "DELETE FROM departments WHERE id = ?"
        self.database.execute(query, (department_id))