# app/ports/employee_repository.py
from abc import ABC, abstractmethod
from domain.models.employee import Employee

class EmployeeRepository(ABC):
    
    @abstractmethod
    def save(self, employee: Employee):
        pass

    @abstractmethod
    def find_by_id(self, employee_id: int) -> Employee:
        pass

    @abstractmethod
    def delete(self, employee_id: int):
        pass