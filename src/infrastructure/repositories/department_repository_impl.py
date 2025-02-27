# infrastructure/repositories/department_repository_impl.py
from app.ports.department_repository import DepartmentRepository
from domain.department import Department
from infrastructure.database.database import Database

class DepartmentRepositoryImpl(DepartmentRepository):
    def __init__(self, database: Database):
        self.database = database

    def save(self, department: Department):
        query = "INSERT INTO departments (id, department) VALUES (?, ?)"
        self.database.execute(query, (department.id, department.department))

    def find_by_id(self, department_id: int) -> Department:
        query = "SELECT id, department FROM departments WHERE id = ?"
        self.database.cursor.execute(query, (department_id))
        result = self.database.cursor.fetchone()
        if result:
            return Department(id=result[0], department=result[1])
        return None

    def delete(self, department_id: int):
        query = "DELETE FROM departments WHERE id = ?"
        self.database.execute(query, (department_id))