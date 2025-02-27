# app/ports/analysis_repository.py
from abc import ABC, abstractmethod
from domain.models.analysis_output_1 import AnalysisOutput1
from domain.models.analysis_output_2 import AnalysisOutput2
from typing import List

class AnalysisRepository(ABC):
    
    @abstractmethod
    def get_employees_job_quarter(self, year: int) -> List[AnalysisOutput1]:
        pass

    @abstractmethod
    def get_employees_dep_hired(self, year: int) -> List[AnalysisOutput2]:
        pass