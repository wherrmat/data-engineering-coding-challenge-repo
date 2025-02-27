# app/ports/employee_repository.py
from abc import ABC, abstractmethod
from domain.models.employee import Employee
from typing import List

class EmployeeRepository(ABC):
    
    @abstractmethod
    def save(self, employee: Employee):
        pass

    @abstractmethod
    def get_all(self) -> List[Employee]:
        pass

    @abstractmethod
    def delete(self, employee_id: int):
        pass