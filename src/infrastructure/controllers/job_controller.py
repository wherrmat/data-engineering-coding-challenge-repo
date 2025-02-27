# infrastructure/api/controllers/job_controller.py
from flask import Blueprint, request, jsonify
from app.use_cases.job_use_cases import CreateJobUseCase, GetJobUseCase, DeleteJobUseCase
from infrastructure.adapters.job_repository_impl import JobRepositoryImpl
from infrastructure.database.database import Database
import os, csv

job_blueprint = Blueprint('job', __name__)

connection_string = os.getenv("DATABASE_STRING_ODBC_CONNECTION_STRING")
database = Database(connection_string)

upload_folder = os.getenv("UPLOADS_PATH")
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)
    
job_repository = JobRepositoryImpl(database)
create_job_use_case = CreateJobUseCase(job_repository)
get_job_use_case = GetJobUseCase(job_repository)
delete_job_use_case = DeleteJobUseCase(job_repository)

# Create jobs from a JSON body request
@job_blueprint.route('/jobs', methods=['POST'])
def create_jobs():

    try:
        data = request.get_json()

        if not isinstance(data, list):
            return jsonify({"error": "The body must be a list of jobs"}), 400
        
        if len(data) < 1 or len(data) > 1000:
            return jsonify({"error": "You can only insert between 1 and 1000 jobs"}), 400
        
        for index, job in enumerate(data):
            if 'id' not in job or 'job' not in job:
                return jsonify({"error": f"Job at index {index} must have 'id' and 'job' fields"}), 400

        for job in data:
            create_job_use_case.execute(job['id'], job['job'])

        return jsonify({"message": "Jobs succesfully created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Load jobs from a CSV file
@job_blueprint.route('/jobs/csvfile', methods=['POST'])
def upload_csv():
    
    if 'file' not in request.files:
        return jsonify({"error": "No file attached"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

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
                        return jsonify({"error": "There are job without all fields"}), 400
                    
                    create_job_use_case.execute(job[0], job[1])

            os.remove(file_path)
            return jsonify({"message": f"{len(rows)} rows successfully uploaded", "data": rows}), 201
        except Exception as e:
            os.remove(file_path)
            return jsonify({"error": f"Error processing the CSV file: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400


# Get by ID
@job_blueprint.route('/jobs/<int:job_id>', methods=['GET'])
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