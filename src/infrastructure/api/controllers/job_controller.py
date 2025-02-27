# infrastructure/api/controllers/job_controller.py
from flask import Blueprint, request, jsonify
from app.use_cases.job_use_cases import CreateJobUseCase, GetJobUseCase, DeleteJobUseCase
from infrastructure.repositories.job_repository_impl import JobRepositoryImpl
from infrastructure.database.database import Database
import os

job_blueprint = Blueprint('job', __name__)

connection_string = os.getenv("DATABASE_STRING_ODBC_CONNECTION_STRING")

database = Database(connection_string)
job_repository = JobRepositoryImpl(database)
create_job_use_case = CreateJobUseCase(job_repository)
get_job_use_case = GetJobUseCase(job_repository)
delete_job_use_case = DeleteJobUseCase(job_repository)

# Create
@job_blueprint.route('/job', methods=['POST'])
def create_job():
    data = request.get_json()
    id = data.get('id')
    job = data.get('job')

    if not id or not job:
        return jsonify({"error": "Missed necessary fields"}), 400

    try:
        create_job_use_case.execute(id, job)
        return jsonify({"message": "Job succesfully created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get by ID
@job_blueprint.route('/job/<int:job_id>', methods=['GET'])
def get_job(job_id):
    try:
        job = get_job_use_case.execute(job_id)
        if job:
            return jsonify({
                "id": job.id,
                "job": job.job
            }), 200
        else:
            return jsonify({"error": "Job not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Delete
@job_blueprint.route('/job/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    try:
        delete_job_use_case.execute(job_id)
        return jsonify({"message": "Job succesfully deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400