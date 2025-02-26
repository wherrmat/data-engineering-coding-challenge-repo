# infrastructure/repositories/job_repository_impl.py
from domain.ports.job_repository import JobRepository
from domain.models.job import Job
from infrastructure.database.database import Database

class JobRepositoryImpl(JobRepository):
    def __init__(self, database: Database):
        self.database = database

    def save(self, job: Job):
        query = "INSERT INTO jobs (id, job) VALUES (?, ?)"
        self.database.execute(query, (job.id, job.job))

    def find_by_id(self, job_id: int) -> Job:
        query = "SELECT id, job FROM jobs WHERE id = ?"
        self.database.cursor.execute(query, (job_id))
        result = self.database.cursor.fetchone()
        if result:
            return Job(id=result[0], job=result[1])
        return None

    def delete(self, job_id: int):
        query = "DELETE FROM jobs WHERE id = ?"
        self.database.execute(query, (job_id))