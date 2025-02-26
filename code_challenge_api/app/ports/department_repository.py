# app/ports/department_repository.py
from abc import ABC, abstractmethod
from domain.department import Department

class DepartmentRepository(ABC):
    @abstractmethod
    def save(self, department: Department):
        pass

    @abstractmethod
    def find_by_id(self, department_id: int) -> Department:
        pass

    @abstractmethod
    def delete(self, department_id: int):
        pass