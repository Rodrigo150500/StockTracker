from src.model.settings.mongo_db_connection import mongo_db_connection
from src.model.repositories.product_repository import ProductRepository
from src.service.generate_report_stock_service import GenerateReportStockService
from src.use_case.generate_report_stock_use_case import GenerateReportStockUseCase


def generate_report_stock_compose():

    connection = mongo_db_connection.get_db_connection()
    repository = ProductRepository(connection)
    service = GenerateReportStockService(repository)
    use_case = GenerateReportStockUseCase(service)

    return use_case