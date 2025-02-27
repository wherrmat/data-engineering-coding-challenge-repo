# infrastructure/api/controllers/job_controller.py
from flask import Blueprint, request
from app.use_cases.job_use_cases import CreateJobsUseCase, LoadJobsFileUseCase, GetJobsUseCase, DeleteJobsUseCase
from infrastructure.adapters.job_repository_impl import JobRepositoryImpl
from infrastructure.database.database import Database
import os

upload_folder = os.getenv("UPLOADS_PATH")
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

job_blueprint = Blueprint('job', __name__)

connection_string = os.getenv("DATABASE_ODBC_CONNECTION_STRING")
database = Database(connection_string)
    
job_repository = JobRepositoryImpl(database)

create_jobs_use_case = CreateJobsUseCase(job_repository)
load_jobs_file_use_case = LoadJobsFileUseCase(job_repository)
get_jobs_use_case = GetJobsUseCase(job_repository)
delete_jobs_use_case = DeleteJobsUseCase(job_repository)

# Create jobs from a JSON body request
@job_blueprint.route('/jobs', methods=['POST'])
def create_jobs():
    return create_jobs_use_case.execute(request=request)

# Load jobs from a CSV file
@job_blueprint.route('/jobs/csvfile', methods=['POST'])
def upload_departmetns_file():
    return load_jobs_file_use_case.execute(request=request)

# Get all jobs
@job_blueprint.route('/jobs', methods=['GET'])
def get_jobS():
    return get_jobs_use_case.execute()

# Delete
@job_blueprint.route('/jobs', methods=['DELETE'])
def delete_jobs():
    return delete_jobs_use_case.execute(request=request)