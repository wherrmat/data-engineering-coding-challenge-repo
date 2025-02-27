# app/use_cases/analysis_use_cases.py
from flask import jsonify
from domain.ports.analysis_repository import AnalysisRepository

class GetEmployeesJobQuarterUseCase:
    def __init__(self, analysis_repository: AnalysisRepository):
        self.analysis_repository = analysis_repository

    def execute(self, year: int):
        try:
            
            if year < 1900 or year > 2999:
                return jsonify({"error": "Invalid year, valid year should be between 1900 and 2900"}), 400
            
            response_items = self.analysis_repository.get_employees_job_quarter(year=year)
            
            if response_items:
                items_list = [{"department": item.department, "job": item.job, "q1": item.q1, "q2": item.q2, "q3": item.q3, "q4": item.q4} for item in response_items]
                return jsonify(items_list), 200
            else:
                return jsonify({"error": f"No items for year {year}"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

class GetEmployeesDepartmentHiredUseCase:
    def __init__(self, analysis_repository: AnalysisRepository):
        self.analysis_repository = analysis_repository

    def execute(self, year: int):
        try:
            
            if year < 1900 or year > 2999:
                return jsonify({"error": "Invalid year, valid year should be between 1900 and 2900"}), 400
            
            response_items = self.analysis_repository.get_employees_dep_hired(year=year)
            
            if response_items:
                items_list = [{"id": item.id, "department": item.department, "hired": item.hired} for item in response_items]
                return jsonify(items_list), 200
            else:
                return jsonify({"error": f"No items for year {year}"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500