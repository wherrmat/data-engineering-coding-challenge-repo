# infrastructure/repositories/analysis_repository_impl.py
from domain.ports.analysis_repository import AnalysisRepository
from domain.models.analysis_output_1 import AnalysisOutput1
from domain.models.analysis_output_2 import AnalysisOutput2
from infrastructure.database.database import Database
from typing import List

class AnalysisRepositoryImpl(AnalysisRepository):
    def __init__(self, database: Database):
        self.database = database

    def get_employees_job_quarter(self, year: int) -> List[AnalysisOutput1]:
        query = f"""
        select
            d.department as department, 
            j.job as job,
            sum(case when datepart(quarter, cast(datetime as DATETIME)) between 1 and 3 THEN 1 else 0 end) as q1,
            sum(case when datepart(quarter, cast(datetime as DATETIME)) between 4 and 6 THEN 1 else 0 end) as q2,
            sum(case when datepart(quarter, cast(datetime as DATETIME)) between 7 and 9 THEN 1 else 0 end) as q3,
            sum(case when datepart(quarter, cast(datetime as DATETIME)) between 10 and 12 THEN 1 else 0 end) as q4
        from [dbo].[hired_employees] e
        join [dbo].[departments] d on e.department_id = d.id
        join [dbo].[jobs] j on e.job_id = j.id
        where year(cast(datetime as DATETIME)) = ?
        group by department, job order by department, job;
        """
        result = self.database.fetch_all(query, (year,)) 
        return result if result else None
    
    def get_employees_dep_hired(self, year: int) -> List[AnalysisOutput2]:
        query = f"""
        with employees_count as (
            select department_id, count(id) as num_employees
            from [dbo].[hired_employees]
            where year(cast(datetime as DATETIME)) = ?
            group by department_id
        ),
        average_hired as (
            select top 1 avg(num_employees) over() as mean_hired from employees_count
        )
        select
            ec.department_id as id,
            d.department as department,
            ec.num_employees as hired
        from employees_count ec
        cross join average_hired ah
        join [dbo].[departments] d on ec.department_id=d.id
        where ec.num_employees > ah.mean_hired
        order by ec.num_employees desc;
        """
        result = self.database.fetch_all(query, (year,))
        return result if result else None