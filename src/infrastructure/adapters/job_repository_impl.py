# infrastructure/repositories/job_repository_impl.py
from domain.ports.job_repository import JobRepository
from domain.models.job import Job
from infrastructure.database.database import Database
from typing import List

class JobRepositoryImpl(JobRepository):
    def __init__(self, database: Database):
        self.database = database

    def save(self, job: Job):
        query = "INSERT INTO jobs (id, job) VALUES (?, ?)"
        self.database.execute(query, (job.id, job.job))

    def get_all(self) -> List[Job]:
        query = "SELECT id, job FROM jobs"
        result = self.database.fetch_all(query)
        return result if result else None

    def delete(self, job_id: int):
        query = "DELETE FROM jobs WHERE id = ?"
        self.database.execute(query, (job_id))