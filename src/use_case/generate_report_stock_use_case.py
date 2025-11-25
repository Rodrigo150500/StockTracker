from io import BytesIO

from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse

from src.service.interfaces.generate_report_stock_service_interface import GenerateReportStockServiceInterface

class GenerateReportStockUseCase:

    def __init__(self, service: GenerateReportStockServiceInterface):
        
        self.__service = service
    

    def handle(self, http_request: HttpRequest) -> HttpResponse:

        xlsx_file = http_request.body

        report_response = self.__service.generate_report(xlsx_file)

        formatted_response = self.__format_response(report_response)

        return formatted_response
    
    
    def __format_response(self, report: BytesIO) -> HttpResponse:

        return HttpResponse(
            body=report,
            status_code= 200
        )