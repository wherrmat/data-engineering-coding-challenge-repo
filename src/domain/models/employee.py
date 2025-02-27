# domain/employee.py

class Employee:
    def __init__(self, id: int, name: str, datetime: str, department_id: int, job_id: int):
        self.id = id
        self.name = name
        self.datetime = datetime
        self.department_id = department_id
        self.job_id = job_id