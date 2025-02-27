# app/use_cases/job_use_cases.py
from domain.job import Job
from app.ports.job_repository import JobRepository

# Create
class CreateJobUseCase:
    def __init__(self, job_repository: JobRepository):
        self.job_repository = job_repository

    def execute(self, id: int, job_name: str):
        job = Job(id=id, job=job_name)
        self.job_repository.save(job)

# Get by ID
class GetJobUseCase:
    def __init__(self, job_repository: JobRepository):
        self.job_repository = job_repository

    def execute(self, job_id: int):
        return self.job_repository.find_by_id(job_id)

# Delete
class DeleteJobUseCase:
    def __init__(self, job_repository: JobRepository):
        self.job_repository = job_repository

    def execute(self, job_id: int):
        self.job_repository.delete(job_id)