# app/ports/job_repository.py
from abc import ABC, abstractmethod
from domain.job import Job

class JobRepository(ABC):
    @abstractmethod
    def save(self, job: Job):
        pass

    @abstractmethod
    def find_by_id(self, job_id: int) -> Job:
        pass

    @abstractmethod
    def delete(self, job_id: int):
        pass