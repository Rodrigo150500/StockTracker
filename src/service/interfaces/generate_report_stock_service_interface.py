from abc import ABC, abstractmethod
from werkzeug.datastructures import FileStorage

class GenerateReportStockServiceInterface(ABC):

    @abstractmethod
    def generate_report(self, xlsx_file: FileStorage) -> dict:
        pass