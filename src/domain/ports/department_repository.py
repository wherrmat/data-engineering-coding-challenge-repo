# app/ports/department_repository.py
from abc import ABC, abstractmethod
from domain.models.department import Department
from typing import List

class DepartmentRepository(ABC):
    
    @abstractmethod
    def save(self, department: Department):
        pass

    @abstractmethod
    def get_all(self) -> List[Department]:
        pass

    @abstractmethod
    def delete(self, department_id: int):
        pass