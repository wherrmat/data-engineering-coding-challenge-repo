# infrastructure/api/controllers/analysis_controller.py
from flask import Blueprint
from app.use_cases.analysis_use_cases import GetEmployeesJobQuarterUseCase, GetEmployeesDepartmentHiredUseCase
from infrastructure.adapters.analysis_repository_impl import AnalysisRepositoryImpl
from infrastructure.database.database import Database
import os

analysis_blueprint = Blueprint('analysis', __name__)

connection_string = os.getenv("DATABASE_STRING_ODBC_CONNECTION_STRING")
database = Database(connection_string)
    
analysis_repository = AnalysisRepositoryImpl(database)

get_employees_job_quarter_use_case = GetEmployeesJobQuarterUseCase(analysis_repository)
get_employees_dep_hired_use_case = GetEmployeesDepartmentHiredUseCase(analysis_repository)

# Get number of employees hired for each job and department by a year, divided by quarter.
@analysis_blueprint.route('/req1/<int:year>', methods=['GET'])
def create_jobs(year):
    return get_employees_job_quarter_use_case.execute(year=year)

# Get List of ids, name and number of employees hired of each department, greater than the mean of employees hired in a year for all the departments
@analysis_blueprint.route('/req2/<int:year>', methods=['GET'])
def upload_departmetns_file(year):
    return get_employees_dep_hired_use_case.execute(year=year)
