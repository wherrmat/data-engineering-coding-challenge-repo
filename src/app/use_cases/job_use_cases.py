# app/use_cases/job_use_cases.py
from flask import Request, jsonify
from domain.models.job import Job
from domain.ports.job_repository import JobRepository
import os, csv

# Create
class CreateJobsUseCase:
    def __init__(self, job_repository: JobRepository):
        self.job_repository = job_repository

    def execute(self, request: Request):
        try:
            data = request.get_json()
            
            if not isinstance(data, list):
                return jsonify({"error": "The body must be a list of jobs"}), 400
            
            if len(data) < 1 or len(data) > 1000:
                return jsonify({"error": "You can only insert between 1 and 1000 jobs"}), 400
            
            for index, item in enumerate(data):
                if item[0] is None or item[1] is None:
                    return jsonify({"error": f"job at index {index} must have 'id' and 'job' fields"}), 400

            for item in data:
                self.job_repository.save(Job(id=item[0], job=item[1]))
            
            return jsonify({"message": "Jobs succesfully created"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

class LoadJobsFileUseCase:
    def __init__(self, job_repository: JobRepository):
        self.job_repository = job_repository

    def execute(self, request: Request):
        if 'file' not in request.files:
            return jsonify({"error": "No file attached"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No attached file"}), 400

        if file and file.filename.endswith('.csv'):
            file_path = os.path.join(os.getenv("UPLOADS_PATH"), file.filename)
            file.save(file_path)

            try:
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    csvreader = csv.reader(csvfile)
                    rows = [row for row in csvreader]
                    csvfile.close()

                    if len(rows) < 1 or len(rows) > 1000:
                        os.remove(file_path)
                        return jsonify({"error": "You can only attach files with 1 - 1000 records"}), 400
                    
                    for job in rows:
                        if len(job) != 2:
                            return jsonify({"error": "There are jobs without all fields"}), 400
                        
                        self.job_repository.save(Job(id=job[0], job=job[1]))

                os.remove(file_path)
                return jsonify({"message": f"{len(rows)} rows successfully uploaded", "data": rows}), 201
            except Exception as e:
                os.remove(file_path)
                return jsonify({"error": f"Error processing the CSV file: {str(e)}"}), 500
        else:
            return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400

# Get all
class GetJobsUseCase:
    def __init__(self, job_repository: JobRepository):
        self.job_repository = job_repository

    def execute(self):
        try:
            jobs = self.job_repository.get_all()
            if jobs:
                jobs_list = [{"id": job.id, "job": job.job} for job in jobs]
                return jsonify(jobs_list), 200
            else:
                return jsonify({"error": "No jobs"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Delete
class DeleteJobsUseCase:
    def __init__(self, job_repository: JobRepository):
        self.job_repository = job_repository

    def execute(self, request: Request):
        try:
            data = request.get_json()
            
            if not isinstance(data, list):
                return jsonify({"error": "The body must be a list of job_id"}), 400
            
            if len(data) < 1 or len(data) > 1000:
                return jsonify({"error": "You can only delet between 1 and 1000 jobs"}), 400
            
            for job_id in data:
                self.job_repository.delete(job_id)
            
            return jsonify({"message": "jobs succesfully deleted"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500