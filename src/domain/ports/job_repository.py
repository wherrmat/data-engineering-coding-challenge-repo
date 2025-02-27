# app/ports/job_repository.py
from abc import ABC, abstractmethod
from domain.models.job import Job
from typing import List

class JobRepository(ABC):
    
    @abstractmethod
    def save(self, job: Job):
        pass

    @abstractmethod
    def get_all(self) -> List[Job]:
        pass

    @abstractmethod
    def delete(self, job_id: int):
        pass