# domain/employee.py

class Employee:
    def __init__(self, id: int, name: str, date_time: str, department_id: int, job_id: int):
        self.id = id
        self.name = name
        self.date_time = date_time
        self.department_id = department_id
        self.job_id = job_id